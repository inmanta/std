import os
import subprocess
import uuid
from typing import Generator

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

    subprocess.run(
        [
            "sudo",
            "docker",
            "cp",
            f"{docker_id}:/module/std/junit.xml",
            f"junit_centos_{centos_version}.xml",
        ],
        check=True,
    )
    no_clean = os.getenv("INMANTA_NO_CLEAN", "false").lower() == "true"
    print(f"Skipping cleanup: {no_clean}")
    if not no_clean:
        subprocess.run(["sudo", "docker", "stop", f"{docker_id}"], check=True)
