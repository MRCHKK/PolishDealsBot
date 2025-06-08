"""Base scraper interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
import logging
import requests
from bs4 import BeautifulSoup

from src.models.offer import Offer
from src.utils.decorators import retry_on_failure


class BaseScraper(ABC):
    """Abstract base class for all scrapers."""

    def __init__(self, name: str):
        """Initialize scraper with name."""
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/121.0.0.0 Safari/537.36"
            )
        }

    @retry_on_failure(max_attempts=3, delay=1.0)
    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse webpage."""
        self.logger.debug(f"Fetching page: {url}")
        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    @abstractmethod
    def parse_offers(self, soup: BeautifulSoup) -> List[Offer]:
        """Parse offers from BeautifulSoup object."""
        pass

    def scrape(self, url: str) -> List[Offer]:
        """Scrape offers from URL."""
        try:
            soup = self.fetch_page(url)
            offers = self.parse_offers(soup)

            # Add source to offers
            for offer in offers:
                object.__setattr__(offer, 'source', self.name)

            self.logger.info(f"Scraped {len(offers)} offers")
            return offers

        except Exception as e:
            self.logger.error(f"Error scraping {self.name}: {e}")
            raise