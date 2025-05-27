"""
Copyright 2025 Inmanta

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

import time
import urllib

import pytest
from pytest_inmanta.plugin import Project
from pytest_inmanta_lsm.remote_orchestrator import RemoteOrchestrator

from inmanta import const

try:
    from inmanta.references import Reference, reference  # noqa: F401
except ImportError:
    pytestmark = pytest.skip(
        "Reference are not yet supported by this core version", allow_module_level=True
    )


def test_references_resource(project: Project, monkeypatch) -> None:

    project.compile(
        """
            import std::testing
            metavalue = std::create_environment_reference("METATESTENV")
            value = std::create_environment_reference(metavalue)
            std::testing::NullResource(agentname="test", name="aaa", value=value)

            # Test that identical references are the same value for the compiler
            value = std::create_environment_reference(metavalue)
        """
    )

    project.deploy_resource_v2(
        "std::testing::NullResource",
        name="aaa",
        expected_status=const.ResourceState.failed,
    )

    monkeypatch.setenv("METATESTENV", "TESTENV")
    monkeypatch.setenv("TESTENV", "testvalue")

    project.compile(
        """
            import std::testing
            metavalue = std::create_environment_reference("METATESTENV")
            value = std::create_environment_reference(metavalue)
            std::testing::NullResource(agentname="test", name="aaa", value=value)
        """
    )

    result = project.deploy_resource_v2("std::testing::NullResource", name="aaa")
    assert result.assert_has_logline("Observed value: testvalue")


def test_fact_references(
    project: Project, remote_orchestrator: RemoteOrchestrator
) -> None:

    def get_resource_status(name: str) -> str:
        """
        Get the status of a resouce in the remote orchestrator
        """
        resource_id = f"std::testing::NullResource[test,name={name}]"
        resp = remote_orchestrator.session.get(
            f"/api/v2/resource/{urllib.parse.quote(resource_id, safe="")}",
            headers={"X-Inmanta-tid": str(remote_orchestrator.environment)},
        )
        resp.raise_for_status()
        return resp.json()["data"]["status"]

    def wait_for_resource(name: str) -> str:
        """
        Wait for the resource to have run
        """
        while get_resource_status(name) not in ["deployed", "failed", "skipped"]:
            time.sleep(0.2)
            pass

    project.compile(
        """
            import unittest
            import std::testing
            resource_a = std::testing::NullResource(agentname="test", name="aaa", value="aaa")

            resource_b = std::testing::NullResource(
                agentname="test",
                name="bbb",
                value=std::create_fact_reference(
                    resource=resource_a,
                    fact_name="my_fact",
                )
            )
        """,
        export=True,
    )

    version = project.version
    assert version is not None

    wait_for_resource("aaa")
    assert get_resource_status("aaa") == "deployed"
    wait_for_resource("bbb")
    assert get_resource_status("bbb") == "failed"

    # We set the fact on the "aaa" resource
    remote_orchestrator.session.put(
        "/api/v2/facts/my_fact",
        headers={"X-Inmanta-tid": str(remote_orchestrator.environment)},
        json={
            "source": "fact",
            "value": "string",
            "resource_id": "std::testing::NullResource[test,name=aaa]",
            "recompile": False,
            "expires": False,
        },
    )

    # We action a deploy (so no need of recompile)
    remote_orchestrator.session.post(
        "/api/v1/deploy",
        headers={"X-Inmanta-tid": str(remote_orchestrator.environment)},
    )

    # Now the resource is deployed
    wait_for_resource("bbb")
    assert get_resource_status("bbb") == "deployed"
