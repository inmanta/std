pipeline {
  agent any
  triggers {
    pollSCM '* * * * *'
  }
  stages {
      stage("build"){
        sh "vagrant up"
      }
  }
  post{
    always{
      sh "vagrant destroy"
    }
  }
}
