pipeline {
  agent any
  triggers {
    pollSCM '* * * * *'
  }
  options { disableConcurrentBuilds() }
  parameters {
    string(name: 'pypi_index', defaultValue: 'https://pypi.org/simple', description: 'Changes the index used to install pytest-inmanta (And only pytest-inmanta)')
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
          ${WORKSPACE}/env/bin/pip install pytest-inmanta -i ${PIP_INDEX_URL}
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
          uuid=$(uuidgen)
          sudo docker build . -t test-module-std-${uuid}
          sudo docker run -t -d --rm --privileged --build-arg PYPI_INDEX=${pypi_index} -v /sys/fs/cgroup:/sys/fs/cgroup:ro test-module-std-${uuid} > docker_id
          sudo docker exec -ti $(cat docker_id) env/bin/pytest tests
          '''
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
