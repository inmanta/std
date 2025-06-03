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


def test_int_reference(project: Project, monkeypatch) -> None:

    project.compile(
        """
            import std
            import std::testing

            str_value = std::create_environment_reference("ENV_VALUE")
            value = std::create_int_reference(str_value)
            std::testing::NullResource(agentname="test", name="abc", int_value=value)

        """
    )
    monkeypatch.setenv("ENV_VALUE", "42")

    result = project.deploy_resource_v2("std::testing::NullResource", name="abc")
    assert result.assert_has_logline("Observed int value: 42")


def test_fact_references(project: Project) -> None:

    model = """
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
        """
    project.compile(model)

    project.deploy_resource_v2(
        "std::testing::NullResource",
        name="aaa",
        expected_status=const.ResourceState.deployed,
    )

    project.deploy_resource_v2(
        "std::testing::NullResource",
        name="bbb",
        expected_status=const.ResourceState.failed,
    )

    a_resource = project.get_resource("std::testing::NullResource", name="aaa")
    project.add_fact(a_resource.id, "my_fact", value="my_value")
    project.compile(model)

    result = project.deploy_resource_v2(
        "std::testing::NullResource",
        name="bbb",
        expected_status=const.ResourceState.deployed,
    )
    assert result.assert_has_logline("Observed value: my_value")
