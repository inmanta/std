pipeline {
  agent any
  triggers {
    pollSCM '* * * * *'
  }
  stages {
      stage("build"){
        steps{
          sh "vagrant up"
        } 
      }
  }
  post{
    always{
      sh "vagrant destroy"
    }
  }
}
