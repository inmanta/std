"""
Copyright 2016 Inmanta

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

import logging

from inmanta.agent.handler import CRUDHandler, HandlerContext, provider
from inmanta.resources import (
    IgnoreResourceException,
    ManagedResource,
    PurgeableResource,
    resource,
)

LOGGER = logging.getLogger(__name__)


@resource("std::testing::NullResource", agent="agentname", id_attribute="name")
class Null(ManagedResource, PurgeableResource):
    fields = ("name", "agentname", "fail", "value", "int_value")


@resource("std::AgentConfig", agent="agent", id_attribute="agentname")
class AgentConfig(PurgeableResource):
    """
    A resource that can modify the agentmap for autostarted agents
    """

    fields = ("agentname", "uri", "autostart")

    @staticmethod
    def get_autostart(exp, obj):
        # inmanta-core 15 (ISO8) removed the autostarted_agent_map environment setting, so there is nothing left for a
        # handler to configure and this resource is never exported. The entity itself is kept because its uri is still
        # useful for generating agent configuration files.
        raise IgnoreResourceException()


@provider("std::testing::NullResource", name="null")
class NullProvider(CRUDHandler):
    """Does nothing at all"""

    def read_resource(self, ctx: HandlerContext, resource: PurgeableResource) -> None:
        if resource.fail:
            raise Exception("This resource is set to fail")
        ctx.debug("Observed value: %(value)s", value=resource.value)
        ctx.debug("Observed int value: %(value)s", value=resource.int_value)
        return

    def create_resource(self, ctx: HandlerContext, resource: PurgeableResource) -> None:
        ctx.set_created()

    def delete_resource(self, ctx: HandlerContext, resource: PurgeableResource) -> None:
        ctx.set_purged()

    def update_resource(
        self, ctx: HandlerContext, changes: dict, resource: PurgeableResource
    ) -> None:
        ctx.set_updated()
