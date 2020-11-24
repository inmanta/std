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
