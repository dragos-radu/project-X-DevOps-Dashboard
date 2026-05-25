pipeline {
    agent {
        label 'raspberry-pi'
    }

    environment {
        POSTGRES_DB = 'devops_dashboard'
        POSTGRES_HOST = '127.0.0.1'
        POSTGRES_PORT = '5432'
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
                    docker build -t devops-dashboard-backend:${BUILD_NUMBER} backend
                    docker tag devops-dashboard-backend:${BUILD_NUMBER} devops-dashboard-backend:local
                '''
            }
        }

        stage('Test Backend Docker Container') {
            steps {

                withCredentials([usernamePassword(
                    credentialsId: 'devops-dashboard-db-creds',
                    usernameVariable: 'POSTGRES_USER',
                    passwordVariable: 'POSTGRES_PASSWORD'
                )]) {
                    sh '''
                        export POSTGRES_DB=devops_dashboard
                        export POSTGRES_HOST=127.0.0.1
                        export POSTGRES_PORT=5432

                        docker compose up -d database
                    '''
                }
                sh '''
                    docker rm -f devops-dashboard-backend-test || true

                    docker run -d \
                        --name devops-dashboard-backend-test \
                        -p 8000:8000 \
                        devops-dashboard-backend:local

                    sleep 5

                    curl -f http://localhost:8000/health

                    docker rm -f devops-dashboard-backend-test
                    docker compose down
                '''
            }
        }
    }

    post {
        success {
            echo 'Initial Jenkins pipeline completed successfully.'
        }
        failure {
            echo 'Initial Jenkins pipeline failed.'
        }
    }
}