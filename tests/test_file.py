import getpass
import os
import inmanta

def test_file_read(project, tmpdir):
    """
        Test deploying a file
    """
    user = getpass.getuser()

    project.add_mock_file("files","testfile","test test test")

    test_path_1 = str(tmpdir.join("file1"))
    
    project.compile(
        """
import unittest

host = std::Host(name="server", os=std::linux)
std::ConfigFile(host=host, path="%(path1)s", content=std::file("unittest/testfile"), owner="%(user)s", group="%(user)s")
"""
        % {
            "path1": test_path_1,
            "user": user,
        }
    )

    assert not os.path.exists(test_path_1)

    file1 = project.get_resource("std::ConfigFile", path=test_path_1)
    assert file1.path == test_path_1
    ctx = project.deploy(file1, run_as_root=False)
    assert ctx.status == inmanta.const.ResourceState.deployed
    assert os.path.exists(test_path_1)
    with open(test_path_1, "r") as fd:
        content = fd.read()
        assert content == "test test test"
