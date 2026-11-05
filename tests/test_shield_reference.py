"""
Copyright 2026 Inmanta

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
import re
import shutil
from collections.abc import Iterator

import pytest
from pytest_inmanta.plugin import Project

from inmanta import const

try:
    from inmanta.references import Reference, reference  # noqa: F401
except ImportError:
    pytestmark = pytest.skip(
        "Reference are not yet supported by this core version", allow_module_level=True
    )


MODULE_CF = """
import std

entity Secret extends std::PurgeableResource:
    string name
    string agentname = "test"
    string password
    bool unshield = true
end

index Secret(name)
implement Secret using std::none
"""

MODULE_PY = """
from inmanta.agent.handler import CRUDHandler, HandlerContext, provider
from inmanta.resources import PurgeableResource, resource

import inmanta_plugins.std as std


@resource("shieldtest::Secret", agent="agentname", id_attribute="name")
class Secret(PurgeableResource):
    fields = ("name", "agentname", "password", "unshield")

    @staticmethod
    def get_password(_, entity):
        return std.shield(entity.password)


@provider("shieldtest::Secret", name="shieldtest")
class SecretHandler(CRUDHandler):
    def read_resource(self, ctx: HandlerContext, resource: Secret) -> None:
        ctx.info(
            "Field type: %(type)s", type=type(resource.password).__name__
        )
        if isinstance(resource.password, std.Shielded):
            ctx.info(
                "Reference id: %(id)s", id=str(resource.password.reference_id)
            )
        if resource.unshield:
            ctx.info(
                "Unshielded value: %(value)s",
                value=std.unshield(resource.password, ctx),
            )
            # A second unshield is served from the resource's reference cache
            std.unshield(resource.password, ctx)

    def create_resource(self, ctx: HandlerContext, resource: Secret) -> None:
        ctx.set_created()

    def delete_resource(self, ctx: HandlerContext, resource: Secret) -> None:
        ctx.set_purged()

    def update_resource(self, ctx: HandlerContext, changes: dict, resource: Secret) -> None:
        ctx.set_updated()
"""


@pytest.fixture
def shieldtest(project: Project) -> Iterator[None]:
    project.create_module("shieldtest", initcf=MODULE_CF, initpy=MODULE_PY)
    yield
    module_path = os.path.join(project._test_project_dir, "libs", "shieldtest")
    if os.path.exists(module_path):
        shutil.rmtree(module_path)


def test_shield_not_resolved_before_handler(
    project: Project, shieldtest: None, monkeypatch
) -> None:
    """
    A shielded reference, and the references it depends on, are not resolved unless
    the handler unshields it: the environment variables don't exist.
    """
    monkeypatch.delenv("SHIELD_META", raising=False)
    project.compile("""
        import shieldtest
        name = std::create_environment_reference("SHIELD_META")
        shieldtest::Secret(
            name="a",
            password=std::create_environment_reference(name),
            unshield=false,
        )
    """)

    result = project.deploy_resource_v2("shieldtest::Secret", name="a")
    result.assert_has_logline("Field type: Shielded")


def test_shield_resolved_by_handler(
    project: Project, shieldtest: None, monkeypatch
) -> None:
    """
    The handler gets the value of the shielded reference when it unshields it.
    """
    monkeypatch.setenv("SHIELD_META", "SHIELD_PASSWORD")
    monkeypatch.setenv("SHIELD_PASSWORD", "s3cret")
    project.compile("""
        import shieldtest
        name = std::create_environment_reference("SHIELD_META")
        shieldtest::Secret(name="a", password=std::create_environment_reference(name))
    """)

    result = project.deploy_resource_v2("shieldtest::Secret", name="a")
    result.assert_has_logline("Unshielded value: s3cret")


def test_shield_failure_in_handler(
    project: Project, shieldtest: None, monkeypatch
) -> None:
    """
    A shielded reference that can't be resolved only fails the resource when the
    handler unshields it.
    """
    monkeypatch.delenv("SHIELD_PASSWORD", raising=False)
    project.compile("""
        import shieldtest
        shieldtest::Secret(
            name="a",
            password=std::create_environment_reference("SHIELD_PASSWORD"),
        )
    """)

    project.deploy_resource_v2(
        "shieldtest::Secret", name="a", expected_status=const.ResourceState.failed
    )


def test_shield_reference_id_stable(project: Project, shieldtest: None) -> None:
    """
    The same reference shielded in two resources has the same id, so handlers can
    use it as a cache key without resolving it.
    """
    project.compile("""
        import shieldtest
        password = std::create_environment_reference("SHIELD_PASSWORD")
        shieldtest::Secret(name="a", password=password, unshield=false)
        shieldtest::Secret(name="b", password=password, unshield=false)
        shieldtest::Secret(
            name="c",
            password=std::create_environment_reference("SHIELD_OTHER"),
            unshield=false,
        )
    """)

    def reference_id(name: str) -> str:
        result = project.deploy_resource_v2("shieldtest::Secret", name=name)
        for line in result.logs:
            match = re.fullmatch(r"Reference id: (\S+)", line.msg)
            if match is not None:
                return match.group(1)
        raise AssertionError(f"No reference id logged for {name}")

    assert reference_id("a") == reference_id("b")
    assert reference_id("a") != reference_id("c")


def test_shield_plain_value(project: Project, shieldtest: None) -> None:
    """
    A plain value is not shielded, unshield returns it as it is.
    """
    project.compile("""
        import shieldtest
        shieldtest::Secret(name="a", password="plain")
    """)

    result = project.deploy_resource_v2("shieldtest::Secret", name="a")
    result.assert_has_logline("Field type: str")
    result.assert_has_logline("Unshielded value: plain")
