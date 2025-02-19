"""
Copyright 2019 Inmanta

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

import re

import pytest
from pytest_inmanta.plugin import Project

from inmanta.ast import ExplicitPluginException, ExternalException


def test_select_attr(project):
    project.compile(
        """
    entity Container:
        string field
    end

    implement Container using std::none

    entity Out:
        string[] fields
    end
    implement Out using std::none

    entity Collector:

    end
    implement Collector using std::none

    Collector.containers [0:] -- Container

    c = Collector()
    c.containers += Container(field="A")
    c.containers += Container(field="B")
    c.containers += Container(field="C")

    Out(fields = std::select(c.containers,"field"))

    """
    )

    assert sorted(project.get_instances("__config__::Out")[0].fields) == ["A", "B", "C"]


def test_hostname(project):
    project.compile(
        """
        r = std::hostname("test.something.com")
        r = "test"
        """
    )


def test_prefixlen(project):
    project.compile(
        """
        r = std::prefixlen("192.168.1.100/24")
        r = 24
        """
    )


def test_network_to_prefixlen(project):
    project.compile(
        """
        r = std::prefixlen("192.168.1.0/24")
        r = 24
        """
    )


def test_netmask(project):
    project.compile(
        """
        r = std::netmask("192.168.1.100/24")
        r = "255.255.255.0"
        """
    )


def test_network_address(project):
    project.compile(
        """
        r = std::network_address("192.168.2.10/24")
        r = "192.168.2.0"
        """
    )


def test_prefixlength_to_netmask(project):
    project.compile(
        """
        r = std::prefixlength_to_netmask(20)
        r = "255.255.240.0"
        """
    )


@pytest.mark.parametrize(
    "cidr, idx, result",
    [
        ("192.168.0.0/16", 1, "192.168.0.1"),
        ("192.168.0.0/16", 256, "192.168.1.0"),
        ("2001:0db8:85a3::0/64", 1, "2001:db8:85a3::1"),
        ("2001:0db8:85a3::0/64", 10000, "2001:db8:85a3::2710"),
        ("2001:0db8:85a3::0/64", 100000, "2001:db8:85a3::1:86a0"),
    ],
)
def test_ipindex(project, cidr, idx, result):
    project.compile(
        f"""
        r = std::ipindex("{cidr}", {idx})
        r = "{result}"
        """
    )


@pytest.mark.parametrize(
    "cidr, idx, result",
    [
        ("192.168.22.11", 22, "192.168.22.33"),
        ("192.168.22.250", 22, "192.168.23.16"),
        ("::1", 15, "::10"),
    ],
)
def test_add_to_ip(project, cidr, idx, result):
    project.compile(
        f"""
        r = std::add_to_ip("{cidr}", {idx})
        r = "{result}"
        """
    )


def test_string_plugins(project):
    project.compile(
        """
        l = std::lower("aAbB")
        l = "aabb"

        u = std::upper("aAbB")
        u = "AABB"

        c = std::capitalize("aAbB c")
        c = "Aabb c"
        """
    )


def test_getenv(project: Project, monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Verify the good behavior of all getenv plugins
    """
    # Check that getenv_or_raise raises a plugin exception
    with pytest.raises(
        ExplicitPluginException,
        match="Environment variable NOT_AN_ENV_VAR doesn't exist",
    ):
        project.compile("std::getenv_or_raise('NOT_AN_ENV_VAR')")

    # Check that getenv_or_unknown returns an unknown
    project.compile(
        """
        unknown = std::getenv_or_unknown('NOT_AN_ENV_VAR')

        assert = true
        assert = std::is_unknown(unknown)
        """
    )

    # Check that getenv returns None or a default
    project.compile(
        """
        none = std::getenv('NOT_AN_ENV_VAR')
        none = null

        def = std::getenv('NOT_AN_ENV_VAR', "def")
        def = "def"
        """
    )

    # Check that all getenv plugins return the env var when it is set
    with monkeypatch.context() as ctx:
        ctx.setenv("ENV_VAR", "val")
        project.compile(
            """
            val = "val"
            val = std::getenv("ENV_VAR")
            val = std::getenv_or_unknown("ENV_VAR")
            val = std::getenv_or_raise("ENV_VAR")
            """
        )


def test_len(project) -> None:
    """
    Verify the behavior of the len plugin and contrast it with the count plugin.
    """
    project.compile(
        """
        unknown = int(std::getenv_or_unknown("UNKNOWN_ENV_INT"))

        empty_list = []
        non_empty_list = [1, 2]
        unknown_list = [1, unknown, 2]
        two_unknowns_list = [1, unknown, 2, unknown]

        assert = true

        assert = std::count(empty_list) == 0
        assert = std::len(empty_list) == 0

        assert = std::count(non_empty_list) == 2
        assert = std::len(non_empty_list) == 2

        assert = std::count(unknown_list) == 3
        assert = std::is_unknown(std::len(unknown_list))

        assert = std::count(two_unknowns_list) == 4
        assert = std::is_unknown(std::len(two_unknowns_list))
        """,
    )


def test_json(project: Project) -> None:
    """
    Test the usage of the json plugins
    """
    project.compile(
        """
        d = std::json_loads(s)
        d = {"a": "a", "b": [{"a": "a"}], "int": 0, "float": 1.0, "bool": true}
        s = std::json_dumps(d)
        s = '{"a": "a", "b": [{"a": "a"}], "int": 0, "float": 1.0, "bool": true}'
        """
    )

    # Entities can not be serialized
    with pytest.raises(ExternalException) as exc_info:
        project.compile(
            """
            entity A: end
            std::json_dumps(A())
            """
        )

    exc: ExternalException = exc_info.value
    assert re.match(
        r"@__config__::A [a-f0-9]+ is not JSON serializable",
        str(exc.__cause__),
    )
