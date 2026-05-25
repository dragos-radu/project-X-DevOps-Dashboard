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

        stage('Test Backend with Database') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'devops-dashboard-db-creds',
                    usernameVariable: 'POSTGRES_USER',
                    passwordVariable: 'POSTGRES_PASSWORD'
                )]) {
                    sh '''
                        export POSTGRES_DB=devops_dashboard

                        docker compose down -v || true
                        docker compose up -d --build backend database

                        echo "Waiting for services..."
                        sleep 10

                        curl -f http://localhost:8001/health

                        docker compose down -v
                    '''
                }
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