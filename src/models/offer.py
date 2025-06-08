"""Offer data models."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Offer:
    """Car offer model."""
    title: str
    price: str
    url: str
    publication_time: Optional[str] = None
    source: Optional[str] = None
    scraped_at: datetime = None

    def __post_init__(self):
        """Initialize scraped_at if not provided."""
        if self.scraped_at is None:
            object.__setattr__(self, 'scraped_at', datetime.now())

    @property
    def unique_key(self) -> tuple[str, str]:
        """Generate unique key for offer identification."""
        return (self.title, self.price)

    def to_dict(self) -> dict:
        """Convert offer to dictionary."""
        return {
            "title": self.title,
            "price": self.price,
            "url": self.url,
            "publication_time": self.publication_time,
            "source": self.source,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None
        }