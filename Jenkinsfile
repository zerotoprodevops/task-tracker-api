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
        stage('Update gitops'){
            steps{
                withCredentials([usernamePassword(credentialsId: 'github-token', passwordVariable: 'GIT_PASS', usernameVariable: 'GIT_USER')]) {
                    sh  '''
                        rm -rf task-tracker-gitops
                        # 1. clone the repo
                        git clone https://${GIT_USER}:${GIT_PASS}@github.com/zerotoprodevops/task-tracker-gitops.git
                        cd task-tracker-gitops

                        # 2: Update Values file
                        yq -i ' .api.image.tag = strenv(TAG) | .api.image.tag style="double" ' ./environment/dev-values.yaml 
                        
                        # 3. Push to GitHub
                        git config user.name "Jenkins CI"
                        git config user.email "jenkins@k8cluster.local"
                        git add .
                        git commit -m "Update ne tag"
                        git push origin main
                        '''    
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