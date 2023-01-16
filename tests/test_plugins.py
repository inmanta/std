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
import pytest


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
    assert project.get_plugin_function("hostname")("test.something.com") == "test"


def test_prefixlen(project):
    assert project.get_plugin_function("prefixlen")("192.168.1.100/24") == "24"


def test_network_to_prefixlen(project):
    assert project.get_plugin_function("prefixlen")("192.168.1.0/24") == "24"


def test_netmask(project):
    assert project.get_plugin_function("netmask")("192.168.1.100/24") == "255.255.255.0"


def test_network_address(project):
    assert (
        project.get_plugin_function("network_address")("192.168.2.10/24")
        == "192.168.2.0"
    )


def test_netmask(project):
    assert project.get_plugin_function("prefixlength_to_netmask")(20) == "255.255.240.0"


@pytest.mark.parametrize(
    "cidr, idx, result",
    [
        ("192.168.5.3/16", 1, "192.168.0.1"),
        ("192.168.5.3/16", 256, "192.168.1.0"),
        ("2001:0db8:85a3::8a2e:0370:7334/64", 1, "2001:db8:85a3::1"),
        ("2001:0db8:85a3::8a2e:0370:7334/64", 10000, "2001:db8:85a3::2710"),
        ("2001:0db8:85a3::8a2e:0370:7334/64", 100000, "2001:db8:85a3::1:86a0"),
    ],
)
def test_ipindex(project, cidr, idx, result):
    assert project.get_plugin_function("ipindex")(cidr, idx) == result


def test_add_to_ip(project):
    assert (
        project.get_plugin_function("add_to_ip")("192.168.22.11", 22) == "192.168.22.33"
    )
    assert (
        project.get_plugin_function("add_to_ip")("192.168.22.250", 22)
        == "192.168.23.16"
    )
    assert project.get_plugin_function("add_to_ip")("::1", 15) == "::10"


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
