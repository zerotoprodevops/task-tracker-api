pipeline{
    agent {
        label 'build-vm'
    }
    environment {
        IMAGE = "jyotimanab/task-tracker-api"
        TAG = "${env.BUILD_NUMBER}"
    }

    stages{
        stage('git Checkout'){
            steps{
                git branch: 'main',
                    url: 'https://github.com/zerotoprodevops/task-tracker-api.git'
            }
        }
        stage('Build'){
            steps{
                sh "docker build -t $IMAGE:$TAG ."
            }
        }
        stage('Scan Image'){
            steps{
                sh "TMPDIR=/tempdir trivy image --severity  CRITICAL --exit-code 1 $IMAGE:$TAG"
            }
        }
        stage("Upload Image to Docker Hub"){
            steps{
                
                withDockerRegistry(credentialsId: 'dockerhub-cred', url: '') {
                    sh  """
                        docker push $IMAGE:$TAG
                        docker tag $IMAGE:$TAG $IMAGE:latest
                        docker push $IMAGE:latest
                        """
                }
            }
        }
    }
    post{
        success{
            echo "Image $IMAGE Build successful and uploaded to Docker Repository"
            sh "docker rmi $IMAGE:$TAG $IMAGE:latest"
        }
        failure{
            echo "Pipeline failed: Image $IMAGE:$TAG kept locally for debugging"
        }
    }
}