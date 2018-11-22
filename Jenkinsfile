pipeline {
  agent any
  triggers {
    pollSCM '* * * * *'
  }
  options { disableConcurrentBuilds() }
 
  stages {
    stage("setup"){
      steps{
        script{
          withCredentials([usernamePassword(credentialsId: 'jenkins_on_openstack', passwordVariable: 'OS_PASSWORD', usernameVariable: 'OS_USERNAME')]) {
            sh "vagrant up"
          }
        }
      } 
    }
    stage("test"){
      steps{
        script{
          withCredentials([usernamePassword(credentialsId: 'jenkins_on_openstack', passwordVariable: 'OS_PASSWORD', usernameVariable: 'OS_USERNAME')]) {
            sh "vagrant ssh -c 'cd std; /home/centos/venv/bin/python3 -m pytest tests -s --junitxml=junit.xml'"
            sh "vagrant ssh-config >ssh.conf"
            sh "scp -F ssh.conf default:std/junit.xml ."
          }
        }
      }
    }
  }
  post{
    always{
      script{
        withCredentials([usernamePassword(credentialsId: 'jenkins_on_openstack', passwordVariable: 'OS_PASSWORD', usernameVariable: 'OS_USERNAME')]) {
          junit testResults:"junit.xml", allowEmptyResults: true
          sh "vagrant destroy"
        }
      }
    }
  }

}
