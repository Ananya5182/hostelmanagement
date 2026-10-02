pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    environment {
        // Docker Hub Registry & Image Configuration
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-credentials'
        DOCKERHUB_REGISTRY       = 'docker.io'
        IMAGE_BACKEND            = 'campusstay/hostel-backend'
        IMAGE_FRONTEND           = 'campusstay/hostel-frontend'

        // Supabase Production Credentials (injected via Jenkins Credentials store or environment)
        SUPABASE_URL             = env.SUPABASE_URL ?: 'https://uyiybnpeiwkfedihmnrl.supabase.co'
        SUPABASE_KEY             = env.SUPABASE_KEY ?: ''
    }

    stages {
        // ==========================================
        // 1. Source Code Checkout
        // ==========================================
        stage('Checkout') {
            steps {
                echo "==> Checking out repository source code..."
                checkout scm
            }
        }

        // ==========================================
        // 2. Unit Testing & Reporting
        // ==========================================
        stage('Unit Tests') {
            steps {
                echo "==> Running Pytest unit test suite and generating JUnit XML report..."
                sh '''
                    mkdir -p test-reports
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r backend/requirements.txt
                    PYTHONPATH=backend pytest backend/tests/test_main.py -v --junitxml=test-reports/junit.xml
                '''
            }
            post {
                always {
                    echo "==> Publishing JUnit XML test execution reports..."
                    junit allowEmptyResults: false, testResults: 'test-reports/junit.xml'
                }
            }
        }

        // ==========================================
        // 3. Docker Image Build
        // ==========================================
        stage('Docker Build') {
            steps {
                echo "==> Building Docker images for Backend and Frontend..."
                script {
                    sh """
                        docker build -t ${IMAGE_BACKEND}:${BUILD_NUMBER} -t ${IMAGE_BACKEND}:latest ./backend
                        docker build -t ${IMAGE_FRONTEND}:${BUILD_NUMBER} -t ${IMAGE_FRONTEND}:latest ./frontend
                    """
                }
            }
        }

        // ==========================================
        // 4. Docker Push to Registry
        // ==========================================
        stage('Docker Push') {
            steps {
                echo "==> Authenticating and pushing images to Docker Hub..."
                withCredentials([usernamePassword(
                    credentialsId: env.DOCKERHUB_CREDENTIALS_ID, 
                    usernameVariable: 'DOCKER_USER', 
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh """
                        echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin ${DOCKERHUB_REGISTRY}
                        docker push ${IMAGE_BACKEND}:${BUILD_NUMBER}
                        docker push ${IMAGE_BACKEND}:latest
                        docker push ${IMAGE_FRONTEND}:${BUILD_NUMBER}
                        docker push ${IMAGE_FRONTEND}:latest
                    """
                }
            }
        }

        // ==========================================
        // 5. Automated Deployment
        // ==========================================
        stage('Deploy') {
            steps {
                echo "==> Deploying containerized services via Docker Compose..."
                sh '''
                    docker compose down --remove-orphans || true
                    docker compose up -d --build
                '''
            }
        }

        // ==========================================
        // 6. Post-Deployment Verification
        // ==========================================
        stage('Smoke Test') {
            steps {
                echo "==> Running live smoke tests against deployed application..."
                sh '''
                    echo "Waiting 10s for service healthchecks to stabilize..."
                    sleep 10
                    curl --fail --retry 5 --retry-delay 3 http://localhost:8000/health || exit 1
                    curl --fail --retry 5 --retry-delay 3 http://localhost/ || exit 1
                    echo "All smoke tests PASSED successfully!"
                '''
            }
        }
    }

    post {
        always {
            echo "==> Cleaning up build workspace and temporary artifacts..."
            archiveArtifacts artifacts: 'test-reports/*.xml', allowEmptyArchive: true
            cleanWs notFailBuild: true
        }
        success {
            echo "========================================================"
            echo " CI/CD Pipeline Completed Successfully! Build #${BUILD_NUMBER}"
            echo "========================================================"
        }
        failure {
            echo "========================================================"
            echo " Pipeline FAILED at stage '${env.STAGE_NAME}'. Inspect logs."
            echo "========================================================"
        }
    }
}
