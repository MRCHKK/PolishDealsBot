"""Bot event handlers and offer processing."""
import asyncio
import logging
from datetime import date
from typing import List, Dict
import discord

from src.bot.client import OfferBot
from src.services.offer_service import OfferService
from src.services.scraper_service import ScraperService
from src.storage.csv_storage import CSVStorage
from src.models.offer import Offer
from src.config.settings import settings
from src.config.constants import MessageTemplate, ScraperName
from src.utils.logger import DiscordLogger
from src.utils.decorators import measure_time, async_retry_on_failure


class OfferHandler:
    """Handler for processing and sending offers."""

    def __init__(self, bot: OfferBot):
        """Initialize offer handler."""
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.discord_logger: DiscordLogger = None

        # Initialize services
        storage = CSVStorage()
        self.offer_service = OfferService(storage)
        self.scraper_service = ScraperService()

        # State
        self.last_reset_date = date.today()
        self.running = False

    async def initialize(self, channel: discord.TextChannel) -> None:
        """Initialize handler with Discord channel."""
        self.discord_logger = DiscordLogger(channel)
        await self.offer_service.initialize()

        # Start auto-fetch task
        self.running = True
        asyncio.create_task(self.auto_fetch_loop(channel))

    @measure_time
    async def process_source(
            self,
            source_name: str,
            offers: List[Offer]
    ) -> int:
        """Process offers from a single source."""
        # Filter new offers
        new_offers = self.offer_service.filter_new_offers(offers)

        if not new_offers:
            return 0

        # Send offers to Discord
        for offer in new_offers:
            await self.send_offer_message(offer)

        # Mark as sent
        await self.offer_service.mark_as_sent(new_offers)

        return len(new_offers)

    async def send_offer_message(self, offer: Offer) -> None:
        """Send single offer to Discord channel."""
        # Build publication time line if available
        pub_time_line = ""
        if offer.publication_time:
            pub_time_line = MessageTemplate.PUBLICATION_TIME_LINE.format(
                time=offer.publication_time
            )

        # Format message
        message = MessageTemplate.OFFER_MESSAGE.format(
            title=offer.title,
            price=offer.price,
            publication_time=pub_time_line,
            url=offer.url
        )

        await self.bot.channel.send(message)

    @async_retry_on_failure(max_attempts=3, delay=2.0)
    async def fetch_and_process_all(self) -> None:
        """Fetch and process offers from all sources."""
        # Check for daily reset
        await self.check_daily_reset()

        # Fetch offers from all sources
        all_offers = await self.scraper_service.scrape_all()

        # Process each source
        for source, offers in all_offers.items():
            source_name = self.get_source_display_name(source)

            await self.discord_logger.log(
                MessageTemplate.CHECKING_SOURCE.format(source=source_name)
            )

            try:
                count = await self.process_source(source_name, offers)

                await self.discord_logger.log(
                    MessageTemplate.NEW_OFFERS_SENT.format(
                        count=count,
                        source=source_name
                    )
                )
            except Exception as e:
                await self.discord_logger.log(
                    MessageTemplate.ERROR_FETCHING.format(
                        source=source_name,
                        error=str(e)
                    ),
                    emoji="❌"
                )

    async def check_daily_reset(self) -> None:
        """Check if we need to reset for a new day."""
        today = date.today()
        if today != self.last_reset_date:
            self.last_reset_date = today
            await self.offer_service.refresh_cache()
            await self.discord_logger.log(MessageTemplate.DAILY_RESET)

            # Cleanup old data weekly
            if today.weekday() == 0:  # Monday
                await self.offer_service.cleanup_old_data()

    def get_source_display_name(self, source: str) -> str:
        """Get display name for source."""
        mapping = {
            "otomoto": ScraperName.OTOMOTO,
            "lento": ScraperName.LENTO,
            "autoplac": ScraperName.AUTOPLAC,
            "sprzedajemy": ScraperName.SPRZEDAJEMY
        }
        return mapping.get(source, source.title())

    async def auto_fetch_loop(self, channel: discord.TextChannel) -> None:
        """Main loop for auto-fetching offers."""
        while self.running:
            try:
                await self.fetch_and_process_all()
            except Exception as e:
                self.logger.error(f"Error in auto-fetch loop: {e}", exc_info=True)

            await asyncio.sleep(settings.update_interval_seconds)

    def stop(self) -> None:
        """Stop the handler."""
        self.running = False