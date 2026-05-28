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

        stage('Test Backend with Database using Docker Compose') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'devops-dashboard-db-creds',
                        usernameVariable: 'POSTGRES_USER',
                        passwordVariable: 'POSTGRES_PASSWORD'
                    ),
                    usernamePassword(
                        credentialsId: 'ICLOUD_APP',
                        usernameVariable: 'ICLOUD_USERNAME',
                        passwordVariable: 'ICLOUD_APP_PASSWORD'
                    )
                ]) {
                    sh '''
                        docker compose down -v || true

                        docker compose up -d --build backend database

                        echo "Waiting for backend and database..."
                        sleep 10

                        echo "Checking backend health..."
                        curl -f http://localhost:8001/health
                        echo ""

                        echo "Checking system metrics endpoint..."
                        curl -f http://localhost:8001/metrics/system
                        echo ""

                        echo "Refreshing news from RSS feeds..."
                        curl -f -X POST http://localhost:8001/news/refresh
                        echo ""

                        echo "Checking news list endpoint..."
                        curl -f http://localhost:8001/news
                        echo ""

                        echo "Checking calendar endpoints..."
                        curl -f http://localhost:8001/calendar/calendars
                        echo ""

                        docker compose down -v
                    '''
                }
            }
        }

        stage('Push Backend Image to GHCR') {
            when {
                allOf {
                    branch 'master'
                    anyOf {
                        changeset "backend/**"
                        changeset "docker-compose.yml"
                    }
                }
            }
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

        stage('Create or Update Kubernetes Database Secret') {
            when {
                allOf {
                    branch 'master'
                    anyOf {
                        changeset "backend/**"
                        changeset "k8s/**"
                        changeset "docker-compose.yml"
                    }
                }
            }
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'devops-dashboard-db-creds',
                        usernameVariable: 'POSTGRES_USER',
                        passwordVariable: 'POSTGRES_PASSWORD'
                    ),
                    usernamePassword(
                        credentialsId: 'ICLOUD_APP',
                        usernameVariable: 'ICLOUD_USERNAME',
                        passwordVariable: 'ICLOUD_APP_PASSWORD'
                    )
                ]) {
                    sh '''
                        kubectl apply -f k8s/namespace.yaml

                        set +x

                        kubectl delete secret database-secret \
                            -n ${K8S_NAMESPACE} \
                            --ignore-not-found

                        kubectl create secret generic database-secret \
                            -n ${K8S_NAMESPACE} \
                            --from-literal=POSTGRES_DB=${POSTGRES_DB} \
                            --from-literal=POSTGRES_USER=${POSTGRES_USER} \
                            --from-literal=POSTGRES_PASSWORD=${POSTGRES_PASSWORD}

                        kubectl delete secret icloud-credentials \
                            -n ${K8S_NAMESPACE} \
                            --ignore-not-found

                        kubectl create secret generic icloud-credentials \
                            -n ${K8S_NAMESPACE} \
                            --from-literal=ICLOUD_USERNAME=${ICLOUD_USERNAME} \
                            --from-literal=ICLOUD_APP_PASSWORD=${ICLOUD_APP_PASSWORD}

                        set -x
                    '''
                }
            }
        }

        stage('Create or Update GHCR Pull Secret') {
            when {
                allOf {
                    branch 'master'
                    anyOf {
                        changeset "backend/**"
                        changeset "k8s/**"
                        changeset "docker-compose.yml"
                    }
                }
            }
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
            when {
                allOf {
                    branch 'master'
                    anyOf {
                        changeset "backend/**"
                        changeset "k8s/**"
                        changeset "docker-compose.yml"
                    }
                }
            }
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
            when {
                allOf {
                    branch 'master'
                    anyOf {
                        changeset "backend/**"
                        changeset "k8s/**"
                        changeset "docker-compose.yml"
                    }
                }
            }
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

        stage('Validate Frontend') {
            steps {
                sh '''
                    test -f frontend/main.py
                    test -f frontend/requirements.txt
                    test -d frontend/qml

                    cd frontend
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                    python -m py_compile main.py
                '''
            }
        }

        stage('Deploy PySide6 QML Frontend') {
            when {
                allOf {
                    branch 'master'
                    anyOf {
                        changeset "frontend/**"
                        changeset "scripts/**"
                    }
                }
            }
            steps {
                sh '''
                    echo "Deploying PySide6 QML frontend..."

                    rm -rf /opt/devops-dashboard-ui/*
                    cp -r frontend/* /opt/devops-dashboard-ui/

                    cd /opt/devops-dashboard-ui

                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Configure and Restart Frontend Service') {
            when {
                allOf {
                    branch 'master'
                    anyOf {
                        changeset "frontend/**"
                        changeset "scripts/**"
                    }
                }
            }
            steps {
                sh '''
                    cd /opt/devops-dashboard-ui

                    sudo -n /usr/bin/cp scripts/devops-dashboard-ui.service /etc/systemd/system/devops-dashboard-ui.service

                    sudo -n /usr/bin/systemctl daemon-reload
                    sudo -n /usr/bin/systemctl enable devops-dashboard-ui.service
                    sudo -n /usr/bin/systemctl restart devops-dashboard-ui.service

                    sleep 5

                    sudo -n /usr/bin/systemctl is-active --quiet devops-dashboard-ui.service || {
                        sudo -n /usr/bin/systemctl status devops-dashboard-ui.service --no-pager || true
                        sudo -n /usr/bin/journalctl -u devops-dashboard-ui.service -n 80 --no-pager || true
                        exit 1
                    }
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'
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

                echo "Frontend service status:"
                sudo -n /usr/bin/systemctl status devops-dashboard-ui.service --no-pager || true
            '''
        }
    }
}
