pipeline {
    agent {
        label 'raspberry-pi'
    }

    environment {
        POSTGRES_DB = 'devops_dashboard'
        POSTGRES_HOST = '127.0.0.1'
        POSTGRES_PORT = '5432'

        KUBECONFIG = '/home/jenkins/.kube/config'

        BACKEND_IMAGE = 'devops-dashboard-backend'
        BACKEND_TAG = 'local'

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
                    docker build -t ${BACKEND_IMAGE}:${BUILD_NUMBER} backend
                    docker tag ${BACKEND_IMAGE}:${BUILD_NUMBER} ${BACKEND_IMAGE}:${BACKEND_TAG}
                '''
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

        stage('Import Backend Image into k3s') {
            steps {
                sh '''
                    docker save ${BACKEND_IMAGE}:${BACKEND_TAG} | sudo /usr/local/bin/k3s ctr images import -
                    sudo /usr/local/bin/k3s ctr images list | grep ${BACKEND_IMAGE}
                '''
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

        stage('Deploy to k3s') {
            steps {
                sh '''
                    kubectl apply -f k8s/database-pvc.yaml
                    kubectl apply -f k8s/database-deployment.yaml
                    kubectl apply -f k8s/database-service.yaml
                    kubectl apply -f k8s/backend-deployment.yaml
                    kubectl apply -f k8s/backend-service.yaml
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
                    echo "Checking backend health through NodePort..."
                    sleep 5
                    kubectl get pods -n devops-dashboard -o wide
                    kubectl get svc -n devops-dashboard
                    kubectl logs -n devops-dashboard deployment/backend --tail=50
                    kubectl logs -n devops-dashboard deployment/database --tail=80
                    curl -f http://localhost:30080/health
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