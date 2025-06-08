"""Autoplac scraper implementation."""
from typing import List
from bs4 import BeautifulSoup

from src.scrapers.base import BaseScraper
from src.models.offer import Offer
from src.config.constants import ScraperName


class AutoplacScraper(BaseScraper):
    """Scraper for Autoplac.pl website."""

    def __init__(self):
        """Initialize Autoplac scraper."""
        super().__init__(ScraperName.AUTOPLAC)

    def parse_offers(self, soup: BeautifulSoup) -> List[Offer]:
        """Parse offers from Autoplac search results."""
        offers = []
        offer_cards = soup.find_all("nwa-offer-card-unified")

        for card in offer_cards:
            try:
                offer = self._parse_card(card)
                if offer:
                    offers.append(offer)
            except Exception as e:
                self.logger.warning(f"Error parsing card: {e}")
                continue

        return offers

    def _parse_card(self, card) -> Offer:
        """Parse single card into Offer."""
        title_tag = card.find("p", class_="content__name")
        if not title_tag:
            return None

        title = title_tag.get_text(strip=True)

        # Extract price
        price_tag = card.find("p", class_="price-info__main")
        price = price_tag.get_text(strip=True) if price_tag else "Brak ceny"

        # Extract link
        link_tag = card.find("a")
        link = link_tag.get("href") if link_tag else ""
        if link.startswith("/"):
            link = f"https://autoplac.pl{link}"

        return Offer(
            title=title,
            url=link,
            price=price,
            publication_time=None  # Autoplac doesn't show publication time
        )