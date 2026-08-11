"""
Copyright 2023 Inmanta

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

from inmanta.module import Project


def test_agent_config_is_never_exported(project: Project):
    """
    std::AgentConfig no longer configures anything on the orchestrator, so no resource is ever exported for it,
    not even for a host with remote_agent set.
    """
    project.compile("""
        import std

        host = std::Host(
            name="test",
            ip="127.0.0.1",
            os=std::linux,
        )
    """)
    assert not project.get_resource("std::AgentConfig")

    project.compile("""
        import std

        host = std::Host(
            name="test",
            ip="127.0.0.1",
            os=std::linux,
            remote_agent=true,
        )
    """)
    assert not project.get_resource("std::AgentConfig")


def test_agent_config_uri(project: Project):
    """
    The entity is kept for generating agent configuration files, so its uri is still derived from the host.
    """
    project.compile("""
        import std

        host = std::Host(
            name="test",
            ip="127.0.0.1",
            os=std::linux,
            remote_agent=true,
        )
    """)
    instances = project.get_instances("std::AgentConfig")
    assert len(instances) == 1
    assert instances[0].uri == "ssh://root@127.0.0.1:22?python=python"

    project.compile("""
        import std

        host = std::Host(
            name="test",
            ip="127.0.0.1",
            os=std::OS(name="testos", family=std::unix, python_cmd="test"),
            remote_agent=true,
        )
    """)
    instances = project.get_instances("std::AgentConfig")
    assert len(instances) == 1
    assert instances[0].uri == "ssh://root@127.0.0.1:22?python=test"
