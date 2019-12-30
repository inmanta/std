pipeline {
  agent any
  triggers {
    pollSCM '* * * * *'
    cron(BRANCH_NAME == "master" ? "H H(2-5) * * *": "")
  }
  options { disableConcurrentBuilds() }
  parameters {
    booleanParam(name:"pytest_inmanta_dev" ,defaultValue: false, description: 'Changes the index used to install pytest-inmanta to the inmanta dev index')
  }
  stages {
    stage("setup"){
      steps{
        script{
          sh '''
          python3 -m venv ${WORKSPACE}/env
          ${WORKSPACE}/env/bin/pip install -U pip
          ${WORKSPACE}/env/bin/pip install -r requirements.txt
          ${WORKSPACE}/env/bin/pip install -r requirements.dev.txt
          '''
        }
      }
    }
    stage("code linting"){
      steps{
        script{
          sh'''
          ${WORKSPACE}/env/bin/flake8 plugins tests
          '''
        }
      }
    }
    stage("tests"){
      steps{
        environment {
          BRANCH_NAME_LOWER = GIT_BRANCH.toLowerCase()
        }
        script{
          sh '''
          sudo docker build . -t test-module-std-${BRANCH_NAME_LOWER} --build-arg PYTEST_INMANTA_DEV=${pytest_inmanta_dev}
          sudo docker run -d --rm --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro test-module-std-${GIT_BRANCH#*/} > docker_id
          sudo docker exec $(cat docker_id) env/bin/pytest tests -v --junitxml=junit.xml
          sudo docker cp $(cat docker_id):/module/std/junit.xml junit.xml
          '''
          junit 'junit.xml'
        }
      }
    }
  }
  post {
    always {
      script {
        if (fileExists('docker_id')) {
          sh'''
          sudo docker stop $(cat docker_id) && rm docker_id
          '''
        }
      }
    }
  }
}
