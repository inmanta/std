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


def test_resources(project):
    """
    Test compiling a simple model that uses std
    """
    project.compile(
        """
import unittest

host = std::Host(name="server", os=std::linux)
file = std::ConfigFile(host=host, path="/tmp/test", content="1234")
        """
    )

    assert len(project.resources) == 1
