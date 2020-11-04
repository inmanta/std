"""
    Copyright 2020 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
import os
import subprocess

import pytest


@pytest.mark.skipif(
    not os.getenv("INMANTA_TEST_INFRA_SETUP", "false").lower() == "true",
    reason="Only run when test infra environment variable is set to true",
)
def test_docker(docker_container):
    print(f"Running tests in container {docker_container}")
    process = subprocess.Popen(
        [
            "sudo",
            "docker",
            "exec",
            f"{docker_container}",
            "env/bin/pytest",
            "tests/",
            "-v",
            "--junitxml=junit.xml",
        ],
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    with process.stdout:
        for line in iter(process.stdout):
            print(line.decode("utf-8").strip())

    exitcode = process.wait()

    assert exitcode == 0, f"The process ended up with a bad return code: {exitcode}"
