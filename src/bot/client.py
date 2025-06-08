"""Discord bot client."""
import discord
import logging
from typing import Optional

from src.config.settings import settings
from src.config.constants import MessageTemplate


class OfferBot(discord.Client):

    def __init__(self):
        intents = discord.Intents.default()
        intents.messages = True
        intents.guilds = True
        intents.message_content = True

        super().__init__(intents=intents)
        self.logger = logging.getLogger(__name__)
        self.channel: Optional[discord.TextChannel] = None

    async def on_ready(self) -> None:
        self.logger.info(MessageTemplate.BOT_LOGGED_IN.format(user=self.user))

        self.channel = self.get_channel(settings.discord_channel_id)
        if not self.channel:
            self.logger.error(f"Channel {settings.discord_channel_id} not found")
            await self.close()
            return

        self.logger.info(MessageTemplate.BOT_STARTED)

        self.dispatch('bot_initialized', self.channel)

    async def on_error(self, event: str, *args, **kwargs) -> None:
        self.logger.error(f"Discord error in {event}", exc_info=True)