pipeline {
  agent {
    docker {
      image 'ssh_and_python'
      args '-u jenkins'
    }
  }
  triggers {
    pollSCM '* * * * *'
  }
  stages {
      stage("build"){
        steps{
          sh "/home/jenkins/venv/bin/python -m pytest tests"
        }
      }
  }
}