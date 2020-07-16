import os
import subprocess
import uuid
from pathlib import Path
from typing import Generator
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


@pytest.fixture(scope="function", params=[7, 8])
def docker_container(request: SubRequest) -> Generator[str, None, None]:
    centos_version = request.param
    pytest_inmanta_dev = os.getenv("PYTEST_INMANTA_DEV", "false")
    print(f"Using the dev index for pytest-inmanta: {pytest_inmanta_dev}")
    image_name = f"test-module-std-{uuid.uuid4()}"
    print(f"Building docker image with name: {image_name}")
    subprocess.run(
        [
            "sudo",
            "docker",
            "build",
            ".",
            "-t",
            image_name,
            "--build-arg",
            f"PYTEST_INMANTA_DEV={pytest_inmanta_dev}",
            "-f",
            f"./dockerfiles/centos{centos_version}.Dockerfile",
        ],
        check=True,
    )
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
            stderr=subprocess.PIPE,
            check=True,
        )
        .stdout.decode("utf-8")
        .strip()
    )
    print(f"Started container with id {docker_id}")
    yield docker_id

    junit_file = f"junit_centos_{centos_version}.xml"
    subprocess.run(
        ["sudo", "docker", "cp", f"{docker_id}:/module/std/junit.xml", junit_file],
        check=True,
    )
    merge_to_junit_xml(junit_file, f"centos-{centos_version}")
    no_clean = os.getenv("INMANTA_NO_CLEAN", "false").lower() == "true"
    print(f"Skipping cleanup: {no_clean}")
    if not no_clean:
        subprocess.run(["sudo", "docker", "stop", f"{docker_id}"], check=True)
