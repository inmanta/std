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
import pytest


def test_file(project, tmpdir):
    """
        Test deploying a file
    """
    # TODO: check reported changes
    # TODO: check changing user, group and mode
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
    with open(test_path_1, "r") as fd:
        content = fd.read()
        assert content == "file1"

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


def test_directory(project, tmpdir):
    test_path_1 = str(tmpdir.join("dir1"))
    project.compile("""
import unittest

host = std::Host(name="server", os=std::linux)
std::Directory(host=host, path="%s", owner="root", group="root", mode="755")
        """ % (test_path_1))

    assert not os.path.exists(test_path_1)
    d1 = project.get_resource("std::Directory", path=test_path_1)
    assert d1.path == test_path_1
    ctx = project.deploy(d1, run_as_root=True)
    assert ctx.status == inmanta.const.ResourceState.deployed
    assert os.path.isdir(test_path_1)


def test_symlink(project, tmpdir):
    test_path_1 = str(tmpdir.join("sym1"))
    project.compile("""
import unittest

host = std::Host(name="server", os=std::linux)
std::Symlink(host=host, source="/dev/null", target="%s")
        """ % (test_path_1))

    assert not os.path.exists(test_path_1)
    s1 = project.get_resource("std::Symlink", target=test_path_1)
    ctx = project.deploy(s1)
    assert ctx.status == inmanta.const.ResourceState.deployed

    assert os.path.islink(test_path_1)
    assert os.readlink(test_path_1) == "/dev/null"

    project.compile("""
import unittest

host = std::Host(name="server", os=std::linux)
std::Symlink(host=host, source="/dev/random", target="%s")
        """ % (test_path_1))

    s1 = project.get_resource("std::Symlink", target=test_path_1)
    ctx = project.deploy(s1)
    assert ctx.status == inmanta.const.ResourceState.deployed

    assert os.path.islink(test_path_1)
    assert os.readlink(test_path_1) == "/dev/random"


def test_symlink_purge(project, tmpdir):
    """
        Test removing a symlink
    """
    test_path_1 = str(tmpdir.join("sym1"))
    os.symlink("/dev/null", test_path_1)

    project.compile("""
import unittest

host = std::Host(name="server", os=std::linux)
std::Symlink(host=host, source="/dev/null", target="%s", purged=true)
        """ % (test_path_1))

    s1 = project.get_resource("std::Symlink", target=test_path_1)
    ctx = project.deploy(s1)
    assert ctx.status == inmanta.const.ResourceState.deployed
    assert not os.path.exists(test_path_1)

    ctx = project.deploy(s1)
    assert ctx.status == inmanta.const.ResourceState.deployed


class SystemdMock(object):
    def __init__(self, io):
        self._io = io
        self._name = "test"
        self._systemd_path = None

        if self._io.file_exists("/usr/bin/systemctl"):
            self._systemd_path = "/usr/bin/systemctl"

        elif self._io.file_exists("/bin/systemctl"):
            self._systemd_path = "/bin/systemctl"

        assert self._systemd_path is not None

    def setup(self):
        self._io.put("/etc/systemd/system/%s.service" % self._name, """
[Unit]
Description=Test daemon
Before=default.target

[Service]
ExecStart=/bin/sleep 12345

[Install]
WantedBy=default.target
""")
        self._io.run(self._systemd_path, ["daemon-reload"])

    def clean(self):
        self._io.remove("/etc/systemd/system/%s.service" % self._name)
        self._io.run(self._systemd_path, ["daemon-reload"])

    def is_active(self):
        return self._io.run(self._systemd_path, ["is-active", "%s.service" % self._name])[2] == 0

    def is_enabled(self):
        return self._io.run(self._systemd_path, ["is-enabled", "%s.service" % self._name])[2] == 0


@pytest.fixture
def systemd(project):
    systemd = SystemdMock(project.io(run_as_root=True))
    systemd.setup()

    yield systemd

    systemd.clean()


def test_systemd_service(project, systemd):
    """
        Test deploying systemd
    """
    # TODO: test reload
    project.compile("""
import unittest

host = std::Host(name="server", os=std::linux)
svc = std::Service(host=host, name="test", state="running", onboot=true)
""")

    svc = project.get_resource("std::Service", name="test")
    ctx = project.deploy(svc, run_as_root=True)
    assert ctx.status == inmanta.const.ResourceState.deployed

    assert systemd.is_enabled()
    assert systemd.is_active()

    project.compile("""
import unittest

host = std::Host(name="server", os=std::linux)
svc = std::Service(host=host, name="test", state="stopped", onboot=true)
""")

    svc = project.get_resource("std::Service", name="test")
    ctx = project.deploy(svc, run_as_root=True)
    assert ctx.status == inmanta.const.ResourceState.deployed

    assert systemd.is_enabled()
    assert not systemd.is_active()

    project.compile("""
import unittest

host = std::Host(name="server", os=std::linux)
svc = std::Service(host=host, name="test", state="stopped", onboot=false)
""")

    svc = project.get_resource("std::Service", name="test")
    ctx = project.deploy(svc, run_as_root=True)
    assert ctx.status == inmanta.const.ResourceState.deployed

    assert not systemd.is_enabled()
    assert not systemd.is_active()