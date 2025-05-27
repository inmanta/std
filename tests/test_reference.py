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

import pytest
from pytest_inmanta.plugin import Project

from inmanta import const
from pytest_inmanta_lsm.remote_orchestrator import RemoteOrchestrator
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


def test_fact_references(project: Project, remote_orchestrator: RemoteOrchestrator) -> None:

    project.compile(
        """
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
    breakpoint()