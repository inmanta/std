import pytest
from pytest_inmanta.plugin import Project

from inmanta.ast import PluginException


def test_references_resource(project: Project, monkeypatch) -> None:

    with pytest.raises(PluginException):
        # Annoying little detail about pytest-inmanta:
        # When pytest-inmanta runs its compile run
        # it serialize and de-serializes all resource
        # i.e. it resolves all references
        # i.e. it fails to compile if the reference are not resolvable on the compiler side
        project.compile(
            """
                import std::testing
                metavalue = std::create_environment_reference("METATESTENV")
                value = std::create_environment_reference(metavalue)
                std::testing::NullResource(agentname="test", name="aaa", value=value)
            """
        )
        # result = project.deploy_resource_v2(
        # "std::testing::NullResource", name="aaa", expected_status=const.ResourceState.failed)

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
