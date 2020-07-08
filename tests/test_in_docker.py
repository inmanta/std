import logging
import os
import subprocess

import pytest

LOGGER = logging.getLogger(__name__)


@pytest.mark.skipif(
    not os.getenv("INMANTA_TEST_INFRA_SETUP", "false").lower() == "true",
    reason="Only run when env var is set to true",
)
def test_docker(docker_container):
    LOGGER.debug(f"Running tests in container {docker_container}")
    subprocess.check_output(
        [
            "sudo",
            "docker",
            "exec",
            f"{docker_container}",
            "env/bin/pytest",
            "tests/",
            "-v",
            "--junitxml=junit.xml",
        ]
    )
