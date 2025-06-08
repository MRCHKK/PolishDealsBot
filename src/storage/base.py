"""Base storage interface."""
from abc import ABC, abstractmethod
from typing import Set, List
from datetime import date

from src.models.offer import Offer


class BaseStorage(ABC):
    """Abstract base class for offer storage."""

    @abstractmethod
    async def load_offers(self, for_date: date = None) -> Set[tuple[str, str]]:
        """Load offers for given date (default: today)."""
        pass

    @abstractmethod
    async def save_offer(self, offer: Offer) -> None:
        """Save single offer."""
        pass

    @abstractmethod
    async def save_offers(self, offers: List[Offer]) -> None:
        """Save multiple offers."""
        pass

    @abstractmethod
    async def cleanup_old_offers(self, days_to_keep: int = 7) -> None:
        """Remove offers older than specified days."""
        pass