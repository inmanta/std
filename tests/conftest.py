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
import sys
from pathlib import Path
from typing import Generator, List
from xml.etree import ElementTree

import pytest
from _pytest.fixtures import SubRequest

collect_ignore = []
if os.getenv("INMANTA_TEST_INFRA_SETUP", "false").lower() == "true":
    # If the INMANTA_TEST_INFRA_SETUP is on, ignore the tests when running outside of docker except the "test_in_docker" one.
    # That test executes the rest of the tests inside a docker container
    # (and skips itself, because the environment variable will be off in the container).
    test_dir = os.path.dirname(os.path.realpath(__file__))
    test_modules = [
        module for module in os.listdir(test_dir) if "test_in_docker" not in module
    ]

    collect_ignore += test_modules


def merge_to_junit_xml(filename: str, suite: str) -> None:
    """
    Takes a junit-xml filename or path to said file.
    From this file it extracts the testsuite node and adds it to the junit_docker.xml file,
    in the process it adds a name to the testsuite (the suite param) and
    changes the classname from tests.* to {suite}.*
    Finaly, it removes the original file.
    This is because jenkins was not handleing multiple junit files being exposed well.
    The classnames are changed so that the tests are grouped by what container they ran in.
    """
    junit_docker = Path("junit_docker.xml")
    if junit_docker.exists():
        tree = ElementTree.parse(junit_docker)
        root = tree.getroot()
        for testsuite in root:
            if testsuite.get("name", None) == suite:
                root.remove(testsuite)

        x_tree = ElementTree.parse(filename)
        x_root = x_tree.getroot()
        x_root[0].attrib["name"] = suite
        fix_classname(x_root[0], suite)
        root.append(x_root[0])

    else:
        tree = ElementTree.parse(filename)
        root = tree.getroot()
        root[0].attrib["name"] = suite
        fix_classname(root[0], suite)

    tree.write(junit_docker)
    os.remove(filename)


def fix_classname(testsuite: ElementTree.Element, suite: str) -> None:
    for element in testsuite:
        element.attrib["classname"] = element.attrib["classname"].replace(
            "tests.", f"{suite}."
        )


@pytest.fixture
def pip_lock_file() -> None:
    """ get all versions of inmanta packages into a freeze file, to make the environment inside docker like the one outside """
    with open("requirements.freeze.all", "w") as ff:
        subprocess.check_call([sys.executable, "-m", "pip", "freeze"], stdout=ff)
    with open("requirements.freeze.tmp", "w") as ff:
        subprocess.check_call(["grep", "inmanta", "requirements.freeze.all"], stdout=ff)
    # pip freeze can produce lines with @ that refer to folders outside the container
    # see also https://github.com/pypa/pip/issues/8174
    # also ignore inmanta-dev-dependencies as this is pinned in the requirements.dev.txt
    with open("requirements.freeze", "w") as ff:
        subprocess.check_call(
            [
                "grep",
                "-v",
                "-e",
                "@",
                "-e",
                "inmanta-dev-dependencies",
                "-e",
                "inmanta-module-",
                "requirements.freeze.tmp",
            ],
            stdout=ff,
        )
    yield


def _get_dockerfiles_for_test() -> List[str]:
    """
    Return the list of docker files that should be used to run the tests against.
    """
    project_root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    dockerfiles_dir = os.path.join(project_root_dir, "dockerfiles")
    if sys.version_info[0:2] == (3, 6):
        return [os.path.join(dockerfiles_dir, "centos7.Dockerfile")]
    elif sys.version_info[0:2] == (3, 9):
        return [os.path.join(dockerfiles_dir, "rocky8.Dockerfile")]
    else:
        raise Exception(
            "Running the tests with INMANTA_TEST_INFRA_SETUP=true is only support using a python3.6 or python3.9 venv"
        )


@pytest.fixture(scope="function", params=_get_dockerfiles_for_test())
def docker_container(pip_lock_file, request: SubRequest) -> Generator[str, None, None]:
    docker_file = request.param
    docker_file_name = os.path.basename(docker_file).split(".")[0]
    image_name = f"test-module-std-{docker_file_name}"

    docker_build_cmd = ["sudo", "docker", "build", ".", "-t", image_name]
    pip_index_url = os.environ.get("PIP_INDEX_URL", None)
    if pip_index_url is not None:
        docker_build_cmd.append("--build-arg")
        docker_build_cmd.append(f"PIP_INDEX_URL={pip_index_url}")
    pip_pre = os.environ.get("PIP_PRE", None)
    if pip_pre is not None:
        docker_build_cmd.append("--build-arg")
        docker_build_cmd.append(f"PIP_PRE={pip_pre}")

    docker_build_cmd.append("-f")
    docker_build_cmd.append(f"./dockerfiles/{os.path.basename(docker_file)}")
    print(docker_build_cmd)

    print(f"Building docker image with name: {image_name}")
    subprocess.run(docker_build_cmd, check=True)
    docker_id = (
        subprocess.run(
            [
                "sudo",
                "docker",
                "run",
                "-d",
                "--rm",
                "--privileged",
                "-v",
                "/sys/fs/cgroup:/sys/fs/cgroup:ro",
                image_name,
            ],
            stdout=subprocess.PIPE,
            check=True,
        )
        .stdout.decode("utf-8")
        .strip()
    )
    print(f"Started container with id {docker_id}")
    yield docker_id

    junit_file = f"junit_{docker_file_name}.xml"
    subprocess.run(
        ["sudo", "docker", "cp", f"{docker_id}:/module/std/junit.xml", junit_file],
        check=True,
    )
    merge_to_junit_xml(junit_file, f"{docker_file_name}")
    no_clean = os.getenv("INMANTA_NO_CLEAN", "false").lower() == "true"
    print(f"Skipping cleanup: {no_clean}")
    if not no_clean:
        subprocess.run(["sudo", "docker", "stop", f"{docker_id}"], check=True)
