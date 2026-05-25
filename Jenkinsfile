pipeline {
    agent {
        label 'raspberry-pi'
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
                sh '''
                    docker rm -f devops-dashboard-backend-test || true

                    docker run -d \
                        --name devops-dashboard-backend-test \
                        -p 8000:8000 \
                        devops-dashboard-backend:local

                    sleep 5

                    curl -f http://localhost:8000/health

                    docker rm -f devops-dashboard-backend-test
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