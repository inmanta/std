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

    out = project.get_stdout()
    assert out.splitlines() == ["testfile1", "testfile2"]
