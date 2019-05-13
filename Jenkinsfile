pipeline {
  agent any
  triggers {
    pollSCM '* * * * *'
    cron("H H(2-5) * * *")
  }
  options { disableConcurrentBuilds() }
  environment {
        OS_AUTH_URL         = credentials('jenkins_on_openstack_url')
        OS_FLOATING_IP_POOL = credentials('jenkins_on_openstack_floating_ip_pool')
        OS_NETWORK          = credentials('jenkins_on_openstack_network')
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
