pipeline {
    agent {
        docker {
            image 'mcr.microsoft.com/playwright/python:v1.40.0-jammy'   // or a newer matching version
            args '-u root --ipc=host'
        }
    }

    environment {
        DJANGO_ALLOW_ASYNC_UNSAFE = 'true'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                # browsers + system deps are already present in the image
                # playwright install chromium   # optional, can keep if you want
                '''
            }
        }
        
        stage('Run Tests & Coverage') {
            steps {
                sh '''
                . venv/bin/activate
                pytest --junitxml=junit.xml --cov=rental --cov-branch --cov-report=xml --cov-report=html:htmlcov --cov-report=term
                '''
            }
        }
    }
    
    post {
        always {
            junit allowEmptyResults: true, testResults: 'junit.xml'
            publishHTML([
                allowMissing: true,
                alwaysLinkToLastBuild: false,
                keepAll: true,
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'HTML Report',
                reportTitles: 'Coverage'
            ])
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}