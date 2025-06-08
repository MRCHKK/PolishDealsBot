"""Scraper orchestration service."""
import asyncio
import logging
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor

from src.scrapers.base import BaseScraper
from src.scrapers.otomoto import OtomotoScraper
from src.scrapers.lento import LentoScraper
from src.scrapers.autoplac import AutoplacScraper
from src.scrapers.sprzedajemy import SprzedajemyScraper
from src.models.offer import Offer
from src.config.settings import settings


class ScraperService:
    """Service for managing and running scrapers."""

    def __init__(self):
        """Initialize scraper service."""
        self.logger = logging.getLogger(__name__)
        self.scrapers: Dict[str, BaseScraper] = {
            "otomoto": OtomotoScraper(),
            "lento": LentoScraper(),
            "autoplac": AutoplacScraper(),
            "sprzedajemy": SprzedajemyScraper()
        }
        self.executor = ThreadPoolExecutor(max_workers=4)

    def get_scraper_urls(self) -> Dict[str, str]:
        """Get URLs for all scrapers."""
        return {
            "otomoto": settings.get_otomoto_url(),
            "lento": settings.get_lento_url(),
            "autoplac": settings.get_autoplac_url(),
            "sprzedajemy": settings.get_sprzedajemy_url()
        }

    async def scrape_source(self, source: str, url: str) -> List[Offer]:
        """Scrape offers from single source."""
        if source not in self.scrapers:
            raise ValueError(f"Unknown scraper: {source}")

        scraper = self.scrapers[source]
        loop = asyncio.get_event_loop()

        try:
            # Run synchronous scraper in thread pool
            offers = await loop.run_in_executor(
                self.executor,
                scraper.scrape,
                url
            )
            return offers
        except Exception as e:
            self.logger.error(f"Error scraping {source}: {e}")
            return []

    async def scrape_all(self) -> Dict[str, List[Offer]]:
        """Scrape offers from all sources concurrently."""
        urls = self.get_scraper_urls()
        tasks = []

        for source, url in urls.items():
            task = self.scrape_source(source, url)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Map results back to sources
        all_offers = {}
        for (source, _), result in zip(urls.items(), results):
            if isinstance(result, Exception):
                self.logger.error(f"Failed to scrape {source}: {result}")
                all_offers[source] = []
            else:
                all_offers[source] = result

        return all_offers

    def __del__(self):
        """Cleanup executor on deletion."""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=False)