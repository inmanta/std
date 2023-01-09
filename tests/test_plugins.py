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


@pytest.mark.parametrize(
    "ip,is_ok",
    [
        ("192.168.5.3", True),
        ("5236", True),
        ("635.236.45.6", False),
        ("1.1.1.1/32", False),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", False),
    ],
)
def test_ip(project, ip, is_ok):
    run_test(project, "std::ipv4_address", ip, is_ok)


@pytest.mark.parametrize(
    "ip,is_ok",
    [
        ("192.168.5.3", False),
        ("5236/24", False),
        ("635.236.45.6/32", False),
        ("1.1.1.1/32", True),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334/36", False),
    ],
)
def test_cidr(project, ip, is_ok):
    run_test(project, "std::ipv4_cidr", ip, is_ok)


@pytest.mark.parametrize(
    "ip,is_ok",
    [
        ("192.168.5.3", False),
        ("5236", False),
        ("2z01:0db8:85a3:0000:0000:8a2e:0370:7334", False),
        ("2001:0db8:85a3::8a2e:0370:7334", True),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", True),
    ],
)
def test_ip_v6(project, ip, is_ok):
    run_test(project, "std::ipv6_address", ip, is_ok)


@pytest.mark.parametrize(
    "ip,is_ok",
    [
        ("192.168.5.3/32", False),
        ("2z01:0db8:85a3:0000:0000:8a2e:0370:7334/64", False),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334/64", True),
        ("2001:0db8:85a3::8a2e:0370:7334/64", True),
    ],
)
def test_cidr_v6(project, ip, is_ok):
    run_test(project, "std::ipv6_cidr", ip, is_ok)


@pytest.mark.parametrize(
    "ip,is_ok",
    [
        ("192.168.5.3", True),
        ("5236", True),
        ("2z01:0db8:85a3:0000:0000:8a2e:0370:7334", False),
        ("2001:0db8:85a3::8a2e:0370:7334", True),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", True),
    ],
)
def test_ip_v10(project, ip, is_ok):
    run_test(project, "std::ipv_any_address", ip, is_ok)


@pytest.mark.parametrize(
    "ip,is_ok",
    [
        ("192.168.5.3/32", True),
        ("2z01:0db8:85a3:0000:0000:8a2e:0370:7334/64", False),
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334/64", True),
        ("2001:0db8:85a3::8a2e:0370:7334/64", True),
    ],
)
def test_cidr_v10(project, ip, is_ok):
    run_test(project, "std::ipv_any_cidr", ip, is_ok)


def test_is_valid_ip(project):
    ip = "10.20.30.40"
    assert project.get_plugin_function("is_valid_ip")(ip)
    ip = "10.555.30"
    assert not project.get_plugin_function("is_valid_ip")(ip)
    ip = "10.20.30.256"
    assert not project.get_plugin_function("is_valid_ip")(ip)


def test_is_valid_ip_in_model_invalid_ip(project):
    model = """
        import std

        std::is_valid_ip(true)
    """
    assert_compilation_error(project, model, "Invalid value 'True', expected String")


def test_is_valid_cidr_v10(project):
    cidr = "::/0"
    assert project.get_plugin_function("is_valid_cidr_v10")(cidr)
    cidr = "::/128"
    assert project.get_plugin_function("is_valid_cidr_v10")(cidr)
    cidr = "1111::1/128"
    assert project.get_plugin_function("is_valid_cidr_v10")(cidr)
    cidr = "1111::1/129"
    assert not project.get_plugin_function("is_valid_cidr_v10")(cidr)
    cidr = "ftff::1/64"
    assert not project.get_plugin_function("is_valid_cidr_v10")(cidr)


def test_test_is_valid_cidr_v10_in_model_invalid_ip(project):
    model = """
        import std

        std::is_valid_cidr_v10(true)
    """
    assert_compilation_error(project, model, "Invalid value 'True', expected String")


def test_is_valid_ip_v10(project):
    ip = "::"
    assert project.get_plugin_function("is_valid_ip_v10")(ip)
    ip = "1111::1"
    assert project.get_plugin_function("is_valid_ip_v10")(ip)
    ip = "1:fffq::1"
    assert not project.get_plugin_function("is_valid_ip_v10")(ip)
    ip = "1111::fffq"
    assert not project.get_plugin_function("is_valid_ip_v10")(ip)


def test_test_is_valid_ip_v10_in_model_invalid_ip(project):
    model = """
        import std

        std::is_valid_ip_v10(true)
    """
    assert_compilation_error(project, model, "Invalid value 'True', expected String")


def test_is_valid_netmask(project):
    netmask = "255.255.255.0"
    assert project.get_plugin_function("is_valid_netmask")(netmask)
    netmask = "255.255.252.0"
    assert project.get_plugin_function("is_valid_netmask")(netmask)
    netmask = "255.128.0.0"
    assert project.get_plugin_function("is_valid_netmask")(netmask)
    netmask = "255.128.0.255"
    assert not project.get_plugin_function("is_valid_netmask")(netmask)
    netmask = "255.120.0.0"
    assert not project.get_plugin_function("is_valid_netmask")(netmask)


def test_hostname(project):
    hostname = "test"
    fqdn = f"{hostname}.something.com"
    assert project.get_plugin_function("hostname")(fqdn) == hostname


def test_hostname_in_model(project):
    model = """
        import std

        std::hostname(true)
    """
    assert_compilation_error(project, model, "Invalid value 'True', expected String")


def test_network(project):
    ip = "192.168.2.10"
    cidr = "24"
    network_address = "192.168.2.0"
    assert project.get_plugin_function("network")(ip, cidr) == network_address


def test_network_in_model_invalid_ip_address(project):
    model = """
        import std

        std::network("192.168.333.40", "24")
    """
    assert_compilation_error(project, model, "Invalid value '192.168.333.40'")


def test_network_in_model_invalid_cidr(project):
    model = """
        import std

        # Pass cidr as number instead of string
        std::network("192.168.125.40", 24)
    """
    assert_compilation_error(project, model, "Invalid value '24', expected String")


def test_cidr_to_network(project):
    cidr = "192.168.2.10/24"
    network_address = "192.168.2.0"
    assert project.get_plugin_function("cidr_to_network")(cidr) == network_address


def test_cidr_to_network_in_model_invalid_cidr(project):
    model = """
        import std

        std::cidr_to_network(true)
    """
    assert_compilation_error(project, model, "Invalid value 'True', expected String")


def test_netmask(project):
    cidr = 20
    netmask = "255.255.240.0"
    assert project.get_plugin_function("netmask")(cidr) == netmask


def test_netmask_in_model_invalid_type(project):
    model = """
        import std

        # Pass string type instead of number
        std::netmask("16")
    """
    assert_compilation_error(project, model, "Invalid value '16', expected Number")


def test_concat(project):
    host = "ahost"
    domain = "domain.com"
    fqdn = f"{host}.{domain}"
    assert project.get_plugin_function("concat")(host, domain) == fqdn


def test_concat_in_model_invalid_host(project):
    model = """
        import std

        std::concat("a$b", "domain.test")
    """
    assert_compilation_error(project, model, "Invalid value 'a$b'")


def test_concat_in_model_invalid_domain(project):
    model = """
        import std

        std::concat("test", "domain.test!")
    """
    assert_compilation_error(project, model, "Invalid value 'domain.test!'")


def test_net_to_nm(project):
    network_address = "192.168.10.0/24"
    netmask = "255.255.255.0"
    assert project.get_plugin_function("net_to_nm")(network_address) == netmask


def test_net_to_nm_in_model_invalid_network_address(project):
    model = """
        import std

        std::net_to_nm(true)
    """
    assert_compilation_error(project, model, "Invalid value 'True', expected String")


@pytest.mark.parametrize(
    "cidr,ip,prefixlen,netmask,network",
    [
        ("192.168.5.3/16", "192.168.5.3", "16", "255.255.0.0", "192.168.0.0"),
        (
            "2001:0db8:85a3::8a2e:0370:7334/64",
            "2001:db8:85a3::8a2e:370:7334",
            "64",
            "ffff:ffff:ffff:ffff::",
            "2001:db8:85a3::",
        ),
    ],
)
def test_ipnet(project, cidr, ip, prefixlen, netmask, network):
    ipnet = project.get_plugin_function("ipnet")

    assert ipnet(cidr, "ip") == ip
    assert ipnet(cidr, "prefixlen") == prefixlen
    assert ipnet(cidr, "netmask") == netmask
    assert ipnet(cidr, "network") == network
    assert ipnet(cidr, "invalid") is None


def test_ipnet_in_model_invalid_cidr(project):
    model = """
        import std

        # Pass ip instead of cidr
        std::ipnet("192.125.125.22", "ip")
    """
    assert_compilation_error(project, model, "Invalid value '192.125.125.22'")


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
    ipnet = project.get_plugin_function("ipindex")
    assert ipnet(cidr, idx) == result


def test_ipindex_in_model_invalid_cidr(project):
    model = """
        import std

        # Pass ip instead of cidr
        std::ipindex("192.125.125.22", 16)
    """
    assert_compilation_error(project, model, "")


def test_ipindex_in_model_invalid_position(project):
    model = """
        import std

        # Pass position as string type instead of number
        std::ipindex("192.125.125.0/24", "16")
    """
    assert_compilation_error(project, model, "Invalid value '16', expected Number")


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


def test_add_in_model_invalid_ipv4_addr(project):
    model = """
        import std

        std::add("192.125.123.1111", 8)
    """
    assert_compilation_error(project, model, "Invalid value '192.125.123.1111'")


def test_add_in_model_invalid_ipv6_addr(project):
    model = """
        import std

        std::add("ffff::fffff", 128)
    """
    assert_compilation_error(project, model, "Invalid value 'ffff::fffff'")


def test_add_in_model_invalid_n_value(project):
    model = """
        import std

        std::add("ffff::ffff", "128")
    """
    assert_compilation_error(project, model, "Invalid value '128', expected Number")
