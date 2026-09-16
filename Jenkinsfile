pipeline {
    agent any

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
                playwright install chromium
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
            // allowEmptyResults prevents the pipeline from failing just because no report was produced
            junit allowEmptyResults: true, testResults: 'junit.xml'
            
            // allowMissing: true so a failed setup stage doesn’t break the post action
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