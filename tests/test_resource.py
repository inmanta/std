"""
Copyright 2019 Inmanta

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

import inmanta.const


def test_null_resource(project):
    project.compile(
        """
            import std::testing
            std::testing::NullResource()
            std::testing::NullResource(agentname="testx", name="aaa")
            std::testing::NullResource(agentname="testx", name="bbb", fail=true)
            std::testing::NullResource(agentname="p", name="p", purged=true)
        """
    )
    project.deploy_resource("std::testing::NullResource", name="null")
    project.deploy_resource("std::testing::NullResource", name="aaa")
    project.deploy_resource(
        "std::testing::NullResource",
        name="bbb",
        status=inmanta.const.ResourceState.failed,
    )
    project.deploy_resource("std::testing::NullResource", name="p")
