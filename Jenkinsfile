pipeline {
  agent any
  triggers {
    pollSCM '* * * * *'
    cron(BRANCH_NAME == "master" ? "H H(2-5) * * *": "")
  }
  options { disableConcurrentBuilds() }
  parameters {
    string(name: 'pypi_index', defaultValue: 'https://artifacts.internal.inmanta.com/inmanta/stable', description: 'Changes the index used to install pytest-inmanta (And only pytest-inmanta)')
  }
  stages {
    stage("setup"){
      steps{
        script{
          sh '''
          python3 -m venv ${WORKSPACE}/env
          ${WORKSPACE}/env/bin/pip install --upgrade pip
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
        script{
          sh '''
          sudo docker build . -t test-module-std-${GIT_BRANCH#*/} --build-arg PYPI_INDEX=${pypi_index}
          sudo docker run -d --rm --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro test-module-std-${GIT_BRANCH#*/} > docker_id
          sudo docker exec $(cat docker_id) env/bin/pytest tests -v --junitxml=junit.xml
          sudo docker cp $(cat docker_id):/module/std/junit.xml junit
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
