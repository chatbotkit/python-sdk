from __future__ import annotations

from typing import Any

from ._transport import Client, ClientOptions
from .blueprint import BlueprintClient
from .bot import BotClient
from .channel import ChannelClient
from .contact import ContactClient
from .conversation import ConversationClient
from .dataset import DatasetClient
from .event import EventClient
from .file import FileClient
from .graphql import GraphqlClient
from .integration import IntegrationClient
from .magic import MagicClient
from .memory import MemoryClient
from .partner import PartnerClient
from .platform import PlatformClient
from .policy import PolicyClient
from .portal import PortalClient
from .secret import SecretClient
from .skillset import SkillsetClient
from .space import SpaceClient
from .task import TaskClient
from .team import TeamClient
from .usage import UsageClient


class ChatBotKit(Client):
    def __init__(self, options: ClientOptions | None = None, **kwargs: Any) -> None:
        super().__init__(options, **kwargs)

        self.bot = BotClient(self)
        self.conversation = ConversationClient(self)
        self.dataset = DatasetClient(self)
        self.skillset = SkillsetClient(self)
        self.file = FileClient(self)
        self.contact = ContactClient(self)
        self.secret = SecretClient(self)
        self.memory = MemoryClient(self)
        self.blueprint = BlueprintClient(self)
        self.task = TaskClient(self)
        self.team = TeamClient(self)
        self.space = SpaceClient(self)
        self.partner = PartnerClient(self)
        self.policy = PolicyClient(self)
        self.portal = PortalClient(self)
        self.usage = UsageClient(self)
        self.magic = MagicClient(self)
        self.event = EventClient(self)
        self.graphql = GraphqlClient(self)
        self.channel = ChannelClient(self)
        self.platform = PlatformClient(self)
        self.integration = IntegrationClient(self)
