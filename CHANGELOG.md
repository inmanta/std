# Changelog

## v8.7.0 - ?

- Add dict_keys plugin to iterate over dictionary keys.
- Fixed compatibility with ``inmanta-core>=18`` (iso9)
- Added ``report_only`` resource attribute (iso9)

## v8.6.5 - 2025-12-12

- Added .ci file for the tests that verify the compatibility between the module and different versions of the Inmanta orchestrator.

## v8.6.4 - 2025-12-08

- Remove dev dependency wheel

## v8.6.3 - 2025-12-05

- Add the requirements files to the source distribution package

## v8.6.2 - 2025-11-03


## v8.6.1 - 2025-08-29

- Removed py.typed file

## v8.6.0 - 2025-08-29

- Added py.typed file

## v8.5.1 - 2025-07-11

- Migrated to native v2 format. Set minimal Python version to 3.12

## v8.5.0 - 2025-07-02

- Add int and fact reference
- Set ``send_event=true`` by default because it's required for most practical models, and the recently introduced
    ``receive_events`` is a more appropriate setting for most other cases.
- Reject reference values during Jinja template evaluation
- Allow reference values for some basic plugins

## v8.4.2 - 2025-06-03

- Compatibility with Python 3.11, broken in 8.4.1.

## v8.4.1 - 2025-06-03 (yanked: broke compatibility with Python 3.11)

- Refactored Jinja template implementation. Behavior remains identical.

## v8.4.0 - 2025-05-02

- Make sure that identical std::Environment references are seen as identical values by the compiler

## v8.3.2 - 2025-04-08


## v8.3.1 - 2025-03-14

- Skip the tests for the references when running against an old version of inmanta-core that doesn't support references yet.

## v8.3.0 - 2025-03-12

- Add std::format plugin to enjoy advanced python string formatting in the inmanta DSL
- Added create_environment_reference plugin to create reference to environment variables
- Added the 'value' attribute to std::testing::NullResource
- Log warning when environment variable is not found by get_env plugin
- Deprecate get_env_int plugin in favor of int(get_env())

## v8.2.3 - 2025-02-06

- Update README.md

## v8.2.2 - 2025-02-03

- Format code using black 25.1.0

## v8.2.1 - 2025-01-23


## v8.2.0 - 2025-01-21

- Added support for dataclasses, a special type of entity that has a Python counterpart.

## v8.1.0 - 2025-01-16

- Add json serialization and deserialization plugins

## v8.0.0 - 2024-12-12

- The std::AgentConfig handler will act as a no-op when running against an ISO or OSS version that doesn't have the autostart_agent_map environment configuration option anymore. It's recommanded to no longer use this resource in that case.
- Remove deprecated 'offset' parameter in 'sequence' plugin.

## v7.0.0 - 2024-10-14

- Remove usage of number type

### Upgrade procedure
- `std::to_number` plugin has been removed
  - Numbers can be converted into a float by using `float(value)`
  - Numbers can be converted into an integer by using `int(value)`
- `std::OS.version` needs to be converted to a float
- `std::MutableNumber` entity has been removed, new alternatives are available:
  - `std::MutableInt` can be used for mutable integer
  - `std::MutableFloat` can be used for mutable float

## v6.1.0 - 2024-10-07
- Add ``receive_events`` attribute to ``std::Resource``

## v6.0.2 - 2024-10-04

- Update documentation

## v6.0.1 - 2024-09-25

- Update README.md

## v6.0.0 - 2024-08-28

- Remove resources related to files, system packages, systemd

### Upgrade procedure:
- Resources related to files have been moved in `inmanta-module-fs`
- Resources related to system packages have been moved in `inmanta-module-apt` and `inmanta-module-yum`
- Resources related to systemd packages have been moved in `inmanta-module-systemd`

## v5.2.2 - 2024-07-04


## v5.2.1 - 2024-03-29


## v5.2.0 - 2024-03-05

- Allow to render a template based on plugin arguments

## v5.1.1 - 2024-02-19

- remove a todo from the docs

## v5.1.0 - 2024-01-16

- Add limit and ip_address_from_interface plugins and support for keep_prefix on ipindex

## v5.0.0 - 2023-12-07
- Add support to deploy an agentConfig for std::Host

## v4.4.0 - 2023-12-05

- Add len plugin to get the length of a list, conservative with respect to unknowns

## v4.3.5 - 2023-11-21

- Add ``regex_string`` function

## v4.3.4 - 2023-11-10

- Deprecate obsolete plugins.

## v4.3.3 - 2023-11-08

- Add support to std module testing for python 3.11

## v4.3.2 - 2023-10-27

- make version in OS entity a float

## v4.3.1 - 2023-10-25

- fix error with version that should have stayed a number

## v4.3.0 - 2023-10-24

- replace "number" type by "int" type where "number" was used as an "int"

## v4.2.1 - 2023-10-05

- Port std module to validation_type method from inmanta-core

## v4.2.0 - 2023-09-08

- Added the DiscoveryResource entity

## v4.1.10 - 2023-09-06

- Deprecate offset parameter in sequence plugin

## v4.1.9 - 2023-08-31


## v4.1.8 - 2023-06-30


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
