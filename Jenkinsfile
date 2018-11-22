pipeline {
  agent any
  triggers {
    pollSCM '* * * * *'
  }
 
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
            sh "vagrant ssh -c 'cd std; ~/venv/bin/python3 -m pytest tests --junitxml=junit.xml'"
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
          sh "vagrant destroy"
        }
      }
    }
    always{
      junit "junit.xml"
    }
  }

}
