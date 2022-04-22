V3.0.15
- Remove pytest.ini and move its logic to pyproject.toml

V3.0.14
- Add pytest.ini file

V3.0.12
- Improve error message clarity

V3.0.11
- Don't reload services when they are stopped

V3.0.9
- Have dependabot track 3.6 incompatible versions.

V3.0.8
- Select the correct docker container for test runs with INMANTA\_TEST\_INFRA\_SETUP=true based on the version of the venv running the tests.

V3.0.7
- Added support to run the tests against the V2 version of this module.

V3.0.6
- replace centos8 by rocky8 in dockerfiles and tests

V3.0.4
- Added support for pytest-inmanta~=2.0

V3.0.3
-  Improved testing: Ensure asyncpg is installed using a pre-compiled python package

V3.0.2
- Add support for Jinja2 version 3.0

V3.0.1
- Constrain Jinja2~=2.0 because of incompatibility with inmanta-core

V3.0.0
- Set purge\_on\_delete to false by default (#268)

V2.1.9
- Improved testing: prevent double-pinning of inmanta-dev-dependencies

V2.1.8
- Improved testing: prevent too many packages from being installed in the testing container

V2.1.7
- Improved testing: handle pip freeze bug: https://github.com/pypa/pip/issues/8174

V2.1.6
- Un-pin transitive dependencies in requirements.txt for improved backward compatibility

V2.1.5
- Improved testing: ensure inmanta version inside and outside the docker container is the same

V2.1.4
- Added `__len__` to `DictProxy` to allow `{{ mydict | length }}` in templates (#218)

V2.1.3
- Added DictProxy to allow accessing dict items from templates (#20)

V2.1.2
- Fix inconsistent default value warning (#214)

V2.1.1
- Use inmanta-dev-dependencies package

V2.1.0
- Add std::Packages to define multiple packages in a list

V2.0.7
- Add non_empty_string type (#153)

V2.0.6
- Ensure a do_reload() doesn't start a service (#147)

V2.0.5
- Pass PIP_INDEX_URL and PIP_PRE to the docker containers that run the tests.
- Fixed dict value null conversion to None in Jinja template (#97)

V2.0.4
- Add support to run the tests on centos8

V2.0.3
- Add fixtures to run tests in docker container

V2.0.2
- Pin dependencies using ~=

V2.0.1
- Pin transitive dependencies

V2.0.0
- Disallow "internal" agentname in AgentConfig (#88)

V1.5.3
- Fixed yum package installed check on CentOS 8

V1.5.2
 - Removed int typedef because it's a built-in type now (#81)

V1.5.1
 - Updated inmanta.resources import due to name clash.

V1.5.0
 - Added support for using current module in template and file paths
 - Added MutableString, MutableNumber and MutableBool types.

V1.4.1
 - Removed first_of and get plugins

V1.4.0
 - Added support for setting remote python command

V1.2.0
 - Added the types printable_ascii and ascii_word

V1.1.0
 - Re-Added unnecessary removed plugin `assert_function`
 - Added extra types and support for custom constrained types

V1.0.0
 - Removed legacy plugins 'any', 'all', 'each', 'order_by', 'select_attr', 'select_many', 'where', 'where_compare', 'delay', 'assert_function'
 - Added is_unknown plugin

V0.26.0
 - Removed in-band signaling for files
 - Removed snapshot restore functionality
 - Added file integrity check to handler
