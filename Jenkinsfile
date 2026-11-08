pipeline{
    agent {
        label 'build-vm'
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
    }
}