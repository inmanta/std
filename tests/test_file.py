"""
    Copyright 2018 Inmanta

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
import getpass
import os

import pytest

from inmanta.const import ResourceState


def test_file_read(project, tmpdir):
    """
    Test deploying a file
    """
    user = getpass.getuser()

    project.add_mock_file("files", "testfile", "test test test")

    test_path_1 = str(tmpdir.join("file1"))

    project.compile(
        f"""
        import unittest

        host = std::Host(name="server", os=std::linux)
        std::ConfigFile(host=host, path="{test_path_1}", content=std::file("unittest/testfile"), owner="{user}", group="{user}")
        """
    )

    assert not os.path.exists(test_path_1)

    file1 = project.get_resource("std::ConfigFile", path=test_path_1)
    assert file1.path == test_path_1

    ctx_dryrun1 = project.dryrun(file1)
    assert len(ctx_dryrun1.changes) == 1
    assert ctx_dryrun1.changes["purged"].current
    assert not ctx_dryrun1.changes["purged"].desired

    ctx = project.deploy(file1, run_as_root=False)
    assert ctx.status == ResourceState.deployed
    assert os.path.exists(test_path_1)
    with open(test_path_1, "r") as fd:
        content = fd.read()
        assert content == "test test test"

    ctx_dryrun2 = project.dryrun(file1)
    assert not ctx_dryrun2.changes


@pytest.mark.parametrize("current_state_purged", [True, False])
def test_file_purge(project, tmpdir, current_state_purged):
    user = getpass.getuser()

    project.add_mock_file("files", "testfile", "test test test")

    test_path_1 = str(tmpdir.join("file1"))

    if current_state_purged:
        assert not os.path.exists(test_path_1)
    else:
        with open(test_path_1, "w+") as f:
            f.write("test test test")
        os.chmod(test_path_1, 0o644)
        assert os.path.exists(test_path_1)

    project.compile(
        f"""
        import unittest

        host = std::Host(name="server", os=std::linux)
        std::ConfigFile(host=host,
                        path="{test_path_1}",
                        content=std::file("unittest/testfile"),
                        owner="{user}",
                        group="{user}",
                        purged=true)
        """
    )

    file1 = project.get_resource("std::ConfigFile", path=test_path_1)
    assert file1.path == test_path_1

    ctx_dryrun1 = project.dryrun(file1)
    if current_state_purged:
        assert not ctx_dryrun1.changes
    else:
        assert len(ctx_dryrun1.changes) == 1
        assert not ctx_dryrun1.changes["purged"].current
        assert ctx_dryrun1.changes["purged"].desired

    ctx = project.deploy(file1, run_as_root=False)
    assert ctx.status == ResourceState.deployed
    assert not os.path.exists(test_path_1)

    ctx_dryrun2 = project.dryrun(file1)
    assert not ctx_dryrun2.changes


def test_list_files(project):
    project.add_mock_file("files", "testfile1", "test test test")
    project.add_mock_file("files", "testfile2", "test test test")

    project.compile(
        """
        import unittest

        for file in std::list_files("unittest"):
            std::source("unittest/{{file}}")
            std::print(file)
        end
        """
    )

    out = sorted(project.get_stdout().splitlines())
    assert ["testfile1", "testfile2"] == out
