"""Sprzedajemy scraper implementation."""
from typing import List
from bs4 import BeautifulSoup

from src.scrapers.base import BaseScraper
from src.models.offer import Offer
from src.config.constants import ScraperName


class SprzedajemyScraper(BaseScraper):
    """Scraper for Sprzedajemy.pl website."""

    def __init__(self):
        """Initialize Sprzedajemy scraper."""
        super().__init__(ScraperName.SPRZEDAJEMY)

    def parse_offers(self, soup: BeautifulSoup) -> List[Offer]:
        """Parse offers from Sprzedajemy search results."""
        offers = []

        ul = soup.find("ul", class_="list normal")
        if not ul:
            return offers

        for li in ul.find_all("li"):
            if not li.get("id", "").startswith("offer-"):
                continue

            try:
                offer = self._parse_list_item(li)
                if offer:
                    offers.append(offer)
            except Exception as e:
                self.logger.warning(f"Error parsing offer: {e}")
                continue

        return offers

    def _parse_list_item(self, li) -> Offer:
        """Parse single list item into Offer."""
        title_tag = li.find("h2", class_="title")
        if not title_tag:
            return None

        a_title = title_tag.find("a")
        if not a_title:
            return None

        title = a_title.get_text(strip=True)
        link = a_title.get("href", "")

        if link.startswith("/"):
            link = f"https://sprzedajemy.pl{link}"

        # Extract price
        price = self._extract_price(li)

        # Extract publication time
        publication_time = self._extract_publication_time(li)

        return Offer(
            title=title,
            url=link,
            price=price,
            publication_time=publication_time
        )

    def _extract_price(self, li) -> str:
        """Extract price from list item."""
        pricing_div = li.find("div", class_="pricing")
        if pricing_div:
            price_span = pricing_div.find("span", class_="price")
            if price_span:
                return price_span.get_text(strip=True)
        return "Brak ceny"

    def _extract_publication_time(self, li) -> str:
        """Extract publication time from list item."""
        time_div = li.find("div", class_="time-and-verified")
        if time_div:
            time_tag = time_div.find("time", class_="time")
            if time_tag:
                return time_tag.get("datetime", time_tag.get_text(strip=True))
        return "Brak informacji o czasie"