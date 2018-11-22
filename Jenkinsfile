pipeline {
  agent any
  triggers {
    pollSCM '* * * * *'
  }
  withCredentials([usernamePassword(credentialsId: 'jenkins_on_openstack', passwordVariable: 'OS_PASSWORD', usernameVariable: 'OS_USERNAME')]) {
    stages {
      stage("setup"){
        steps{
          sh "vagrant up"
        } 
      }
      stage("test"){
        steps{
          sh "vagrant ssh -c 'cd std; ~/venv/bin/python3 -m pytest tests --junitxml=junit.xml'"
          sh "vagrant ssh-config >ssh.conf"
          sh "scp -F ssh.conf default:std/junit.xml ."
        }
      }
    }
    post{
      always{
        junit "junit.xml"
        sh "vagrant destroy"

      }
    }
  }

  
}
