"""
    Copyright 2017 Inmanta

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


def test_get_facts(project):
    """
    Test mocking out facts during unit tests
    """
    project.add_fact("std::File[test,path=/etc/motd]", "mode", 755)
    project.compile(
        """
    import unittest
    h = std::Host(name="test", os=std::linux)
    f = std::File(host=h, path="/etc/motd", content="", owner="root", group="root")
    f.mode=std::getfact(f, "mode")
    """
    )

    f = project.get_resource("std::File")
    assert f.permissions == 755
