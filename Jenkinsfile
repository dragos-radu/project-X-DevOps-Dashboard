pipeline {
    agent {
        label 'raspberry-pi'
    }

    environment {
        POSTGRES_DB = 'devops_dashboard'
        POSTGRES_HOST = '127.0.0.1'
        POSTGRES_PORT = '5432'

        KUBECONFIG = '/home/jenkins/.kube/config'

        REGISTRY = 'ghcr.io'
        GITHUB_OWNER = 'dragos-radu'
        BACKEND_IMAGE_NAME = 'devops-dashboard-backend'
        BACKEND_IMAGE = "${REGISTRY}/${GITHUB_OWNER}/${BACKEND_IMAGE_NAME}"
        BACKEND_TAG = "${BUILD_NUMBER}"

        K8S_NAMESPACE = 'devops-dashboard'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Backend Docker Image') {
            steps {
                sh '''
                    docker build -t ${BACKEND_IMAGE}:${BACKEND_TAG} backend
                    docker tag ${BACKEND_IMAGE}:${BACKEND_TAG} ${BACKEND_IMAGE}:latest
                '''
            }
        }

        stage('Push Backend Image to GHCR') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-token',
                    usernameVariable: 'GHCR_USER',
                    passwordVariable: 'GHCR_TOKEN'
                )]) {
                    sh '''
                        echo "$GHCR_TOKEN" | docker login ghcr.io -u "$GHCR_USER" --password-stdin

                        docker push ${BACKEND_IMAGE}:${BACKEND_TAG}
                        docker push ${BACKEND_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Test Backend with Database using Docker Compose') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'devops-dashboard-db-creds',
                    usernameVariable: 'POSTGRES_USER',
                    passwordVariable: 'POSTGRES_PASSWORD'
                )]) {
                    sh '''
                        docker compose down -v || true

                        docker compose up -d --build backend database

                        echo "Waiting for backend and database..."
                        sleep 10

                        curl -f http://localhost:8001/health

                        docker compose down -v
                    '''
                }
            }
        }

        stage('Create or Update Kubernetes Database Secret') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'devops-dashboard-db-creds',
                    usernameVariable: 'POSTGRES_USER',
                    passwordVariable: 'POSTGRES_PASSWORD'
                )]) {
                    sh '''
                        kubectl apply -f k8s/namespace.yaml

                        kubectl delete secret database-secret \
                            -n ${K8S_NAMESPACE} \
                            --ignore-not-found

                        kubectl create secret generic database-secret \
                            -n ${K8S_NAMESPACE} \
                            --from-literal=POSTGRES_DB=${POSTGRES_DB} \
                            --from-literal=POSTGRES_USER=${POSTGRES_USER} \
                            --from-literal=POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
                    '''
                }
            }
        }

        stage('Create or Update GHCR Pull Secret') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-token',
                    usernameVariable: 'GHCR_USER',
                    passwordVariable: 'GHCR_TOKEN'
                )]) {
                    sh '''
                        kubectl delete secret ghcr-secret \
                            -n ${K8S_NAMESPACE} \
                            --ignore-not-found

                        kubectl create secret docker-registry ghcr-secret \
                            -n ${K8S_NAMESPACE} \
                            --docker-server=ghcr.io \
                            --docker-username=${GHCR_USER} \
                            --docker-password=${GHCR_TOKEN}
                    '''
                }
            }
        }

        stage('Deploy to k3s') {
            steps {
                sh '''
                    kubectl apply -f k8s/database-pvc.yaml
                    kubectl apply -f k8s/database-deployment.yaml
                    kubectl apply -f k8s/database-service.yaml
                    kubectl apply -f k8s/backend-deployment.yaml
                    kubectl apply -f k8s/backend-service.yaml

                    kubectl set image deployment/backend \
                        backend=${BACKEND_IMAGE}:${BACKEND_TAG} \
                        -n ${K8S_NAMESPACE}
                '''
            }
        }

        stage('Wait for Kubernetes Rollout') {
            steps {
                sh '''
                    kubectl rollout status deployment/database -n ${K8S_NAMESPACE} --timeout=120s
                    kubectl rollout status deployment/backend -n ${K8S_NAMESPACE} --timeout=120s
                '''
            }
        }

        stage('Health Check k3s Backend') {
            steps {
                sh '''
                    echo "Waiting for backend health with database ok..."

                    for i in $(seq 1 30); do
                        RESPONSE=$(curl -s http://localhost:30080/health || true)
                        echo "$RESPONSE"

                        echo "$RESPONSE" | grep '"database":"ok"' && exit 0

                        echo "Backend or database not ready yet. Retry $i/30..."
                        sleep 3
                    done

                    echo "Backend health check failed"
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully. Backend and database deployed to k3s.'
        }

        failure {
            echo 'Pipeline failed. Check logs above.'

            sh '''
                echo "Current Kubernetes resources:"
                kubectl get all -n ${K8S_NAMESPACE} || true

                echo "Backend logs:"
                kubectl logs -n ${K8S_NAMESPACE} deployment/backend --tail=50 || true

                echo "Database logs:"
                kubectl logs -n ${K8S_NAMESPACE} deployment/database --tail=50 || true
            '''
        }
    }
}