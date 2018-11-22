pipeline {
  agent any
  triggers {
    pollSCM '* * * * *'
  }
 
  stages {
    stage("setup"){
      steps{
        withCredentials([usernamePassword(credentialsId: 'jenkins_on_openstack', passwordVariable: 'OS_PASSWORD', usernameVariable: 'OS_USERNAME')]) {
          sh "vagrant up"
        }
      } 
    }
    stage("test"){
      steps{
        withCredentials([usernamePassword(credentialsId: 'jenkins_on_openstack', passwordVariable: 'OS_PASSWORD', usernameVariable: 'OS_USERNAME')]) {
          sh "vagrant ssh -c 'cd std; ~/venv/bin/python3 -m pytest tests --junitxml=junit.xml'"
          sh "vagrant ssh-config >ssh.conf"
          sh "scp -F ssh.conf default:std/junit.xml ."
        }
      }
    }
  }
  post{
    always{
      withCredentials([usernamePassword(credentialsId: 'jenkins_on_openstack', passwordVariable: 'OS_PASSWORD', usernameVariable: 'OS_USERNAME')]) {
        junit "junit.xml"
        sh "vagrant destroy"
      }
    }
  }
  
}
