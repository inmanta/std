import os
import subprocess

import pytest

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


@pytest.fixture
def docker_container(monkeypatch):
    current_branch_name = (
        subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        .decode("utf-8")
        .strip()
    )
    print(f"Running std tests on branch {current_branch_name}")
    pytest_inmanta_dev = os.getenv("PYTEST_INMANTA_DEV", "false")
    print(f"Using the dev index for pytest-inmanta: {pytest_inmanta_dev}")
    subprocess.check_output(
        [
            "sudo",
            "docker",
            "build",
            ".",
            "-t",
            f"test-module-std-{current_branch_name}",
            "--build-arg",
            f"PYTEST_INMANTA_DEV={pytest_inmanta_dev}",
        ]
    )
    docker_id = (
        subprocess.check_output(
            [
                "sudo",
                "docker",
                "run",
                "-d",
                "--rm",
                "--privileged",
                "-v",
                "/sys/fs/cgroup:/sys/fs/cgroup:ro",
                f"test-module-std-{current_branch_name}",
            ]
        )
        .decode("utf-8")
        .strip()
    )
    print(f"Started container with id {docker_id}")
    yield docker_id

    subprocess.check_output(
        ["sudo", "docker", "cp", f"{docker_id}:/module/std/junit.xml", "junit.xml"]
    )
    no_clean = os.getenv("INMANTA_NO_CLEAN", "false").lower() == "true"
    print(f"Skipping cleanup: {no_clean}")
    if not no_clean:
        subprocess.check_output(["sudo", "docker", "stop", f"{docker_id}"])
