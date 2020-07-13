def run_tests_in_container(centos_version) {
  // Docker can only have lower case in it's build tags
  branch_name_lower = env.GIT_BRANCH.toLowerCase()
  container_name = "test-module-std-centos${centos_version}-${branch_name_lower}"
  container_id_file = "docker_id_centos${centos_version}"
  sh (
    script: """
      sudo docker build . -t ${container_name} --build-arg PYTEST_INMANTA_DEV=\${pytest_inmanta_dev}
      sudo docker run -d --rm --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro ${container_name} > ${container_id_file}
      sudo docker exec \$(cat ${container_id_file}) env/bin/pytest tests -v --junitxml=junit.xml
      sudo docker cp \$(cat ${container_id_file}):/module/std/junit.xml junit-centos${centos_version}.xml
    """,
  )
}

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
    stage("Run tests on centos7"){
      steps{
        script{
          run_tests_in_container('7')
          junit 'junit-centos7.xml'
        }
      }
    }
    stage("Run tests on centos8"){
      steps{
        script{
          run_tests_in_container('8')
          junit 'junit-centos8.xml'
        }
      }
    }
  }
  post {
    always {
      script {
        sh'''
          for container_id_file in ./docker_id_centos*; do
            sudo docker stop $(cat ${container_id_file}) && rm ${container_id_file}
          done
        '''
      }
    }
  }
}
