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

from inmanta.ast import RuntimeException


def assert_compilation_error(project, model, error_message):
    exception_occured = False

    try:
        project.compile(model)
    except RuntimeException as e:
        exception_occured = True
        print(e.msg)
        assert error_message in e.msg
    assert exception_occured


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


def run_test(project, thetype, value, is_ok):
    def make():
        project.compile(
            f"""
import std
entity Holder:
    {thetype} value
end
implement Holder using std::none

Holder(value="{value}")
"""
        )

    if not is_ok:
        with pytest.raises(RuntimeException):
            make()
    else:
        make()


def test_hostname(project):
    hostname = "test"
    fqdn = f"{hostname}.something.com"
    assert project.get_plugin_function("hostname")(fqdn) == hostname

def test_cidr_to_prefixlen(project):
    cidr = "192.168.1.100/24"
    prefixlen = "24"
    assert project.get_plugin_function("cidr_to_prefixlen")(cidr) == prefixlen

def test_cidr_to_netmask(project):
    cidr = "192.168.1.100/24"
    netmask = "255.255.255.0"
    assert project.get_plugin_function("cidr_to_netmask")(cidr) == netmask

def test_cidr_to_network_address(project):
    cidr = "192.168.2.10/24"
    network_address = "192.168.2.0"
    assert project.get_plugin_function("cidr_to_network_address")(cidr) == network_address

def test_netmask(project):
    cidr = 20
    netmask = "255.255.240.0"
    assert project.get_plugin_function("netmask")(cidr) == netmask


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
    ipindex = project.get_plugin_function("ipindex")
    assert ipindex(cidr, idx) == result

def test_add(project):
    ip = "192.168.22.11"
    increment = 22
    result = "192.168.22.33"
    assert project.get_plugin_function("add")(ip, increment) == result
    ip = "192.168.22.250"
    increment = 22
    result = "192.168.23.16"
    assert project.get_plugin_function("add")(ip, increment) == result
    ip = "::1"
    increment = 15
    result = "::10"
    assert project.get_plugin_function("add")(ip, increment) == result
