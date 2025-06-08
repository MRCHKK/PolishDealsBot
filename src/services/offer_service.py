"""Offer management service."""
import logging
from typing import List, Set
from datetime import date

from src.models.offer import Offer
from src.storage.base import BaseStorage


class OfferService:
    """Service for managing offers."""

    def __init__(self, storage: BaseStorage):
        """Initialize offer service."""
        self.storage = storage
        self.logger = logging.getLogger(__name__)
        self._sent_offers_cache: Set[tuple[str, str]] = set()
        self._cache_date: date = None

    async def initialize(self) -> None:
        """Initialize service and load existing offers."""
        await self.refresh_cache()

    async def refresh_cache(self) -> None:
        """Refresh sent offers cache."""
        today = date.today()
        if self._cache_date != today:
            self._sent_offers_cache = await self.storage.load_offers(today)
            self._cache_date = today
            self.logger.info(f"Loaded {len(self._sent_offers_cache)} existing offers")

    def filter_new_offers(self, offers: List[Offer]) -> List[Offer]:
        """Filter out already sent offers."""
        new_offers = []
        for offer in offers:
            if offer.unique_key not in self._sent_offers_cache:
                new_offers.append(offer)
        return new_offers

    async def mark_as_sent(self, offers: List[Offer]) -> None:
        """Mark offers as sent."""
        if not offers:
            return

        # Update cache
        for offer in offers:
            self._sent_offers_cache.add(offer.unique_key)

        # Persist to storage
        await self.storage.save_offers(offers)

        self.logger.info(f"Marked {len(offers)} offers as sent")

    async def cleanup_old_data(self, days_to_keep: int = 7) -> None:
        """Clean up old offer data."""
        await self.storage.cleanup_old_offers(days_to_keep)
        self.logger.info(f"Cleaned up offers older than {days_to_keep} days")