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
            python3 -m venv ${WORKSPACE}/env
            ${WORKSPACE}/env/bin/pip install -r requirements.txt
            ${WORKSPACE}/env/bin/pip install -r requirements.dev.txt
            ${WORKSPACE}/env/bin/pip install pytest-inmanta -i ${PIP_INDEX_URL}
        }
      }
    }
    stage("code linting"){
      steps{
        script{
            flake8 plugins tests
        }
    }
    stage("tests"){
      steps{
        script{
          uuid=$(uuidgen)
          docker build . -t test-module-std-${uuid}
          docker run -t -d --rm --privileged --build-arg PYPI_INDEX=${pypi_index} -v /sys/fs/cgroup:/sys/fs/cgroup:ro test-module-std-${uuid} > docker_id
          docker exec -ti $(cat docker_id) env/bin/pytest tests
        }
      }
    }
    post {
      always {
        script {
          [ -f docker_id ] && docker stop $(cat docker_id) && rm docker_id
        }
      }
    }
  }
}
