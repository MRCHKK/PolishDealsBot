"""Otomoto scraper implementation."""
from typing import List
from bs4 import BeautifulSoup

from src.scrapers.base import BaseScraper
from src.models.offer import Offer
from src.config.constants import ScraperName, ErrorMessage


class OtomotoScraper(BaseScraper):
    """Scraper for Otomoto.pl website."""

    def __init__(self):
        """Initialize Otomoto scraper."""
        super().__init__(ScraperName.OTOMOTO)

    def parse_offers(self, soup: BeautifulSoup) -> List[Offer]:
        """Parse offers from Otomoto search results."""
        search_results = soup.find("div", {"data-testid": "search-results"})
        if not search_results:
            raise ValueError(ErrorMessage.NO_SEARCH_RESULTS)

        offers = []
        articles = search_results.find_all("article")[:20]  # Limit to 20 offers

        for article in articles:
            try:
                offer = self._parse_article(article)
                if offer:
                    offers.append(offer)
            except Exception as e:
                self.logger.warning(f"Error parsing article: {e}")
                continue

        return offers

    def _parse_article(self, article) -> Offer:
        """Parse single article into Offer."""
        # Extract title and link
        title_tag = article.find("h2")
        if not title_tag or not title_tag.find("a"):
            return None

        title = title_tag.find("a").text.strip()
        link = title_tag.find("a")["href"]

        # Extract price
        price_tag = article.find("h3", {"data-sentry-element": "Price"})
        price_currency_tag = article.find("p", {"data-sentry-element": "PriceCurrency"})

        if price_tag and price_currency_tag:
            price = f"{price_tag.text.strip()} {price_currency_tag.text.strip()}"
        else:
            price = "Brak ceny"

        # Extract publication time
        publication_time = self._extract_publication_time(article)

        return Offer(
            title=title,
            url=link,
            price=price,
            publication_time=publication_time
        )

    def _extract_publication_time(self, article) -> str:
        """Extract publication time from article."""
        metadata_list = article.find("dl", {"data-sentry-element": "MetaDataList"})
        if metadata_list:
            publication_dds = metadata_list.find_all("dd")
            if len(publication_dds) > 1:
                return publication_dds[1].text.strip()
        return "Brak informacji o czasie"