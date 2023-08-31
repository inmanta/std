# Changelog

## v4.1.8 - ?

- Adjust the .ci configuration file to run the tests using python3.9

## v4.1.7 - 2023-04-18


## v4.1.6 - 2023-04-04


## v4.1.5 - 2023-03-22
- Fixed bug in delete operation of std::testing::NullResource

## v4.1.4 - 2023-03-06
- Add std::testing::NullResource, the resource that does nothing

## v4.1.3 - 2023-02-02


## v4.1.1 - 2023-01-18
- Ported ip plugin to std
- Improve error logging in std::Package

## v4.1.0 - 2023-01-13
- Add upper and lower string functions

## v4.0.1
- Drop is_set plugin

## v4.0.0
- autostart attribute of AgentConfig doesn't allow null as value anymore

## v3.1.3
- Don't allow empty names for ResourceSet

## v3.1.2
- Fix passing Undefined to plugins in templates

## v3.1.1
- Fix environment check for None value

## v3.1.0
- Add ResourceSet entity

## v3.0.16
- Fix tests to support email_validator>=1.2.0

## v3.0.15
- Remove pytest.ini and move its logic to pyproject.toml

## v3.0.14
- Add pytest.ini file

## v3.0.12
- Improve error message clarity

## v3.0.11
- Don't reload services when they are stopped

## v3.0.9
- Have dependabot track 3.6 incompatible versions.

## v3.0.8
- Select the correct docker container for test runs with INMANTA\_TEST\_INFRA\_SETUP=true based on the version of the venv running the tests.

## v3.0.7
- Added support to run the tests against the ## v2 version of this module.

## v3.0.6
- replace centos8 by rocky8 in dockerfiles and tests

## v3.0.4
- Added support for pytest-inmanta~=2.0

## v3.0.3
-  Improved testing: Ensure asyncpg is installed using a pre-compiled python package

## v3.0.2
- Add support for Jinja2 version 3.0

## v3.0.1
- Constrain Jinja2~=2.0 because of incompatibility with inmanta-core

## v3.0.0
- Set purge\_on\_delete to false by default (#268)

## v2.1.9
- Improved testing: prevent double-pinning of inmanta-dev-dependencies

## v2.1.8
- Improved testing: prevent too many packages from being installed in the testing container

## v2.1.7
- Improved testing: handle pip freeze bug: https://github.com/pypa/pip/issues/8174

## v2.1.6
- Un-pin transitive dependencies in requirements.txt for improved backward compatibility

## v2.1.5
- Improved testing: ensure inmanta version inside and outside the docker container is the same

## v2.1.4
- Added `__len__` to `DictProxy` to allow `{{ mydict | length }}` in templates (#218)

## v2.1.3
- Added DictProxy to allow accessing dict items from templates (#20)

## v2.1.2
- Fix inconsistent default value warning (#214)

## v2.1.1
- Use inmanta-dev-dependencies package

## v2.1.0
- Add std::Packages to define multiple packages in a list

## v2.0.7
- Add non_empty_string type (#153)

## v2.0.6
- Ensure a do_reload() doesn't start a service (#147)

## v2.0.5
- Pass PIP_INDEX_URL and PIP_PRE to the docker containers that run the tests.
- Fixed dict value null conversion to None in Jinja template (#97)

## v2.0.4
- Add support to run the tests on centos8

## v2.0.3
- Add fixtures to run tests in docker container

## v2.0.2
- Pin dependencies using ~=

## v2.0.1
- Pin transitive dependencies

## v2.0.0
- Disallow "internal" agentname in AgentConfig (#88)

## v1.5.3
- Fixed yum package installed check on CentOS 8

## v1.5.2
 - Removed int typedef because it's a built-in type now (#81)

## v1.5.1
 - Updated inmanta.resources import due to name clash.

## v1.5.0
 - Added support for using current module in template and file paths
 - Added MutableString, MutableNumber and MutableBool types.

## v1.4.1
 - Removed first_of and get plugins

## v1.4.0
 - Added support for setting remote python command

## v1.2.0
 - Added the types printable_ascii and ascii_word

## v1.1.0
 - Re-Added unnecessary removed plugin `assert_function`
 - Added extra types and support for custom constrained types

## v1.0.0
 - Removed legacy plugins 'any', 'all', 'each', 'order_by', 'select_attr', 'select_many', 'where', 'where_compare', 'delay', 'assert_function'
 - Added is_unknown plugin

## v0.26.0
 - Removed in-band signaling for files
 - Removed snapshot restore functionality
 - Added file integrity check to handler
