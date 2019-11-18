import pytest
from inmanta.ast import AttributeException


@pytest.mark.parametrize("attr_type,value,is_valid", [
    ("std::date", '"2019-03-04"', True),
    ("std::date", '"2019-24-04"', False),
    ("std::time", '"12:33:45"', True),
    ("std::time", '"25:33:45"', False),
    ("std::datetime", '"2019-07-31T02:03:59"', True),
    ("std::datetime", '"2019-07-31T02:03:60"', False),
    ("std::ipv4_address", '"192.168.11.33"', True),
    ("std::ipv4_address", '"192.168.11.256"', False),
    ("std::ipv4_interface", '"192.1.2.3/24"', True),
    ("std::ipv4_interface", '"192.1.2.3/33"', False),
    ("std::ipv4_network", '"192.1.5.0/24"', True),
    ("std::ipv4_network", '"192.1.5.1/24"', False),
    ("std::ipv6_address", '"2001:db8:85a3:8d3:1319:8a2e:370:7348"', True),
    ("std::ipv6_address", '"2001:db8:85a3:8d3:1319:8a2e:370:734z"', False),
    ("std::ipv6_interface", '"2001:db8:85a3:8d3:1319:8a2e:370:7348/64"', True),
    ("std::ipv6_interface", '"2001:db8:85a3:8d3:1319:8a2e:370:7348/129"', False),
    ("std::ipv6_network", '"2001:db8:85a3:8d3::/64"', True),
    ("std::ipv6_network", '"2001:db8:85a3:8d3::1/64"', False),
    ("std::uuid", '"35ea1490-f3d4-4b1d-99e7-52c258f7848e"', True),
    ("std::uuid", '"35ea1490-f3d4-4b1d-99e7-52c258f7848"', False),
    ("std::email_str", '"test@host.com"', True),
    ("std::email_str", '"testhost.com"', False),
    ("std::name_email", '"Test user <test-user@example.com>"', True),
    ("std::name_email", '"Test user <test-user@example.com"', False),
    ("std::any_url", '"ssh://host.com"', True),
    ("std::any_url", '"ssh:/host.com"', False),
    ("std::any_http_url", '"http://host:8080"', True),
    ("std::any_http_url", '"ssh://host:8080"', False),
    ("std::http_url", '"http://host.com:8080"', True),
    ("std::http_url", '"http://host:8080"', False),
    ("std::ipv_any_address", '"192.168.2.11"', True),
    ("std::ipv_any_address", '"192.168.2.1111"', False),
    ("std::ipv_any_interface", '"fe80::1/64"', True),
    ("std::ipv_any_interface", '"fe80::g111/16"', False),
    ("std::ipv_any_network", '"1234::/16"', True),
    ("std::ipv_any_network", '"1234::1/16"', False),
    ("std::negative_float", '-1.2', True),
    ("std::negative_float", '1.2', False),
    ("std::negative_int", '-2', True),
    ("std::negative_int", '0', False),
    ("std::positive_float", '2.6', True),
    ("std::positive_float", '-2.3', False),
    ("std::positive_int", '5', True),
    ("std::positive_int", '0', False),
    ("std::int", '-2', True),
    ("std::int", '-2.1', True),
    ("std::alfanum", '"Qwerty123"', True),
    ("std::alfanum", '"qwerty/123"', False),
    ("std::base64", '"dGVzdA=="', True),
    ("std::base64", '"dGVzdA="', False),
])
def test_attribute_types(project, attr_type, value, is_valid):
    model = f"""
            entity Test:
                {attr_type} attr
            end

            implement Test using std::none

            Test(test={value})
            """
    if is_valid:
        project.compile(model)
    else:
        with pytest.raises(AttributeException):
            project.compile(model)


# * pydantic.condecimal:
#     gt: Decimal = None
#     ge: Decimal = None
#     lt: Decimal = None
#     le: Decimal = None
#     max_digits: int = None
#     decimal_places: int = None
#     multiple_of: Decimal = None
# * pydantic.confloat and pydantic.conint:
#     gt: float = None
#     ge: float = None
#     lt: float = None
#     le: float = None
#     multiple_of: float = None,
# * pydantic.constr:
#     min_length: int = None
#     max_length: int = None
#     curtail_length: int = None (Only verify the regex on the first curtail_length of characters)
#     regex: str = None          (The regex is verified via the behavior of Pattern.match())
# * pydantic.stricturl:
#     min_length: int = 1
#     max_length: int = 2 ** 16
#     tld_required: bool = True
#     allowed_schemes: Optional[Set[str]] = None


@pytest.mark.parametrize("attr_type,base_type,value,validation_parameters,is_valid", [
    ("pydantic.condecimal", "number", 8, '{"gt": 0, "lt": 10}', True),
    ("pydantic.condecimal", "number", 8, '{"gt": 0, "lt": 5}', False),
    ("pydantic.confloat", "number", 1.5, '{"multiple_of": 0.5}', True),
    ("pydantic.confloat", "number", 1.5, '{"multiple_of": 0.2}', False),
    ("pydantic.conint", "number", 4, ''{"ge": 4}, True),
    ("pydantic.conint", "number", 4, ''{"ge": 5}, False),
    ("pydantic.constr", "string", '"test123"', {"regex": "^test.*$"}, True),
    ("pydantic.constr", "string", '"test123"', {"regex": "^tst.*$"}, False),
    ("pydantic.stricturl", "string", '"http://test:8080"', '{"tld_required": false}', True),
    ("pydantic.stricturl", "string", '"http://test:8080"', '{"tld_required": true}', False),
])
def test_constrained_types(project, attr_type, base_type, value, validation_parameters, is_valid):
    model = f"""
            typedef custom_type as {base_type} matching std::validate_type("{attr_type}", self, {validation_parameters})

            entity Test:
                custom_type attr
            end

            implement Test using std::none

            Test(attr={value})
            """
    if is_valid:
        project.compile(model)
    else:
        with pytest.raises(AttributeException):
            project.compile(model)
