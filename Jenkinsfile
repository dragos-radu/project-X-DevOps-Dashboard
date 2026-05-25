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

        stage('Agent Info') {
            steps {
                sh '''
                    echo "Running on Jenkins agent:"
                    hostname
                    whoami
                    pwd
                '''
            }
        }

        stage('Check Tools') {
            steps {
                sh '''
                    git --version
                    python3 --version
                    pip3 --version || true
                '''
            }
        }

        stage('Backend Dependency Check') {
            steps {
                sh '''
                    cd backend
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    python -c "from app.main import app; print('Backend import OK')"
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