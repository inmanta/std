pipeline {
  agent any
  triggers {
    pollSCM '* * * * *'
  }
  options { disableConcurrentBuilds() }
  environment {
        PIP_INDEX_URL='https://artifacts.internal.inmanta.com/inmanta/dev'
  }
  stages {
    stage("setup"){
      steps{
        script{
            python3 -m venv ${WORKSPACE}/env
            ${WORKSPACE}/env/bin/pip install -r requirements.txt
            ${WORKSPACE}/env/bin/pip install -r requirements.dev.txt
            ${WORKSPACE}/env/bin/pip install pytest-inmanta -i ${PIP_INDEX_URL}
        }
      }
    }
    stage("test"){
      steps{
        flake8 plugins tests
        pytest tests -v
      }
    }
  }
}
