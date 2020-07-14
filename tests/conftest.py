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
        .lower()
    )
    print(f"Running std tests on branch {current_branch_name}")
    pytest_inmanta_dev = os.getenv("PYTEST_INMANTA_DEV", "false")
    print(f"Using the dev index for pytest-inmanta: {pytest_inmanta_dev}")
    subprocess.run(
        [
            "sudo",
            "docker",
            "build",
            ".",
            "-t",
            f"test-module-std-{current_branch_name}",
            "--build-arg",
            f"PYTEST_INMANTA_DEV={pytest_inmanta_dev}",
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
                f"test-module-std-{current_branch_name}",
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
            "junit_docker.xml",
        ],
        check=True,
    )
    no_clean = os.getenv("INMANTA_NO_CLEAN", "false").lower() == "true"
    print(f"Skipping cleanup: {no_clean}")
    if not no_clean:
        subprocess.run(["sudo", "docker", "stop", f"{docker_id}"], check=True)
