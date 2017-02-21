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
import inmanta
import os


def test_resources(project):
    """
        Test compiling a simple model that uses std
    """
    project.compile("""
import unittest

host = std::Host(name="server", os=std::linux)
file = std::ConfigFile(host=host, path="/tmp/test", content="1234")
        """)

    assert len(project.resources) == 1


def test_deploy_file(project, tmpdir):
    """
        Test deploying a file
    """
    # TODO: check reported changes
    test_path_1 = str(tmpdir.join("file1"))
    test_path_2 = str(tmpdir.join("file2"))
    file_2_content = "file2 content"
    with open(test_path_2, "w") as fd:
        fd.write(file_2_content)

    test_path_3 = str(tmpdir.join("file3"))
    with open(test_path_3, "w") as fd:
        fd.write("file3 content")

    test_path_4 = str(tmpdir.join("file4"))
    os.mkdir(test_path_4)

    project.compile("""
import unittest

host = std::Host(name="server", os=std::linux)
# create a file
std::ConfigFile(host=host, path="%s", content="file1")
# modify a file
std::ConfigFile(host=host, path="%s", content="file2")
# purge a file
std::ConfigFile(host=host, path="%s", content="file3", purged=true)
# path is a dir
std::ConfigFile(host=host, path="%s", content="file4")
        """ % (test_path_1, test_path_2, test_path_3, test_path_4))

    assert not os.path.exists(test_path_1)
    assert os.path.exists(test_path_2)
    assert os.path.exists(test_path_3)
    assert os.path.exists(test_path_4)

    file1 = project.get_resource("std::File", path=test_path_1)
    assert file1.path == test_path_1
    ctx = project.deploy(file1, run_as_root=True)
    assert ctx.status == inmanta.const.ResourceState.deployed
    assert os.path.exists(test_path_1)

    file2 = project.get_resource("std::File", path=test_path_2)
    ctx = project.deploy(file2, run_as_root=True)
    assert ctx.status == inmanta.const.ResourceState.deployed
    assert os.path.exists(test_path_2)
    with open(test_path_2, "r") as fd:
        content = fd.read()
        assert content != file_2_content
        assert content == "file2"

    file3 = project.get_resource("std::File", path=test_path_3)
    ctx = project.deploy(file3, run_as_root=True)
    assert ctx.status == inmanta.const.ResourceState.deployed
    assert not os.path.exists(test_path_3)

    file4 = project.get_resource("std::File", path=test_path_4)
    ctx = project.deploy(file4)
    assert ctx.status == inmanta.const.ResourceState.failed
