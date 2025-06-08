"""Lento scraper implementation."""
from typing import List
from bs4 import BeautifulSoup

from src.scrapers.base import BaseScraper
from src.models.offer import Offer
from src.config.constants import ScraperName


class LentoScraper(BaseScraper):
    """Scraper for Lento.pl website."""

    def __init__(self):
        """Initialize Lento scraper."""
        super().__init__(ScraperName.LENTO)

    def parse_offers(self, soup: BeautifulSoup) -> List[Offer]:
        """Parse offers from Lento search results."""
        offers = []
        offer_divs = soup.find_all("div", class_="tablelist-tr")

        for offer_div in offer_divs:
            try:
                offer = self._parse_offer_div(offer_div)
                if offer:
                    offers.append(offer)
            except Exception as e:
                self.logger.warning(f"Error parsing offer: {e}")
                continue

        return offers

    def _parse_offer_div(self, offer_div) -> Offer:
        """Parse single offer div into Offer."""
        title_tag = offer_div.find("a", class_="title-list-item")
        if not title_tag:
            return None

        title = title_tag.get_text(strip=True)
        link = title_tag.get("href")

        # Extract price
        price_tag = offer_div.find("span", class_="price-list-item")
        price = price_tag.get_text(strip=True) if price_tag else "Brak ceny"

        # Extract publication time
        pub_div = offer_div.find("div", class_="data-list-item")
        publication_time = pub_div.get_text(" ", strip=True) if pub_div else "Brak informacji o czasie"

        return Offer(
            title=title,
            url=link,
            price=price,
            publication_time=publication_time
        )