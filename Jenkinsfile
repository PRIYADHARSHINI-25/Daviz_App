pipeline {
agent any
    environment {
        scannerHome = tool 'scanner'  // Global declaration if used in multiple stages
    }
    stages { 
        stage('SCM Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/PRIYADHARSHINI-25/Daviz_App'
            }
        }
        stage('Setup Python Environment') {
            steps {
                sh '''
                    echo "passed"
                '''
            }
        }
        stage('Run SonarQube') {
            steps {
                withSonarQubeEnv(credentialsId: 'sonar-proj', installationName: 'SonarQube') {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
            }
        }
        stage('SonarQube Quality Gate Check') {
            steps {
                script {
                    def qualityGate = waitForQualityGate()
                    if (qualityGate.status != 'OK') {
                        echo "Quality Gate Status: ${qualityGate.status}"
                        error "Quality Gate failed: ${qualityGate.status}"
                    } else {
                        echo "Quality Gate Status: ${qualityGate.status}"
                        echo "SonarQube Quality Gates Passed"
                    }
                }
            }
        }
    }
}
