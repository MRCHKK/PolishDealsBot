"""CSV-based storage implementation."""
import csv
import os
from datetime import date, datetime, timedelta
from typing import Set, List
from pathlib import Path
import asyncio
import aiofiles
import aiofiles.os

from src.storage.base import BaseStorage
from src.models.offer import Offer
from src.config.settings import settings


class CSVStorage(BaseStorage):
    """CSV file storage implementation."""

    def __init__(self, filename: str = "offers.csv"):
        """Initialize CSV storage."""
        self.filepath = settings.data_dir / filename
        self.lock = asyncio.Lock()
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Ensure CSV file exists with headers."""
        if not self.filepath.exists():
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["date", "title", "price", "url", "source", "publication_time"])

    async def load_offers(self, for_date: date = None) -> Set[tuple[str, str]]:
        """Load offers for given date."""
        if for_date is None:
            for_date = date.today()

        offers = set()
        date_str = for_date.isoformat()

        async with self.lock:
            if not await aiofiles.os.path.exists(self.filepath):
                return offers

            async with aiofiles.open(self.filepath, mode="r", encoding="utf-8") as f:
                content = await f.read()

        # Process content synchronously
        lines = content.strip().split('\n')
        if len(lines) <= 1:  # Only header or empty
            return offers

        reader = csv.DictReader(lines)
        for row in reader:
            if row.get("date") == date_str:
                offers.add((row["title"], row["price"]))

        return offers

    async def save_offer(self, offer: Offer) -> None:
        """Save single offer."""
        await self.save_offers([offer])

    async def save_offers(self, offers: List[Offer]) -> None:
        """Save multiple offers."""
        if not offers:
            return

        today_str = date.today().isoformat()
        rows = []

        for offer in offers:
            rows.append([
                today_str,
                offer.title,
                offer.price,
                offer.url,
                offer.source or "",
                offer.publication_time or ""
            ])

        async with self.lock:
            async with aiofiles.open(self.filepath, mode="a", encoding="utf-8") as f:
                for row in rows:
                    await f.write(",".join(f'"{field}"' for field in row) + "\n")

    async def cleanup_old_offers(self, days_to_keep: int = 7) -> None:
        """Remove offers older than specified days."""
        cutoff_date = date.today() - timedelta(days=days_to_keep)
        cutoff_str = cutoff_date.isoformat()

        async with self.lock:
            if not await aiofiles.os.path.exists(self.filepath):
                return

            # Read all content
            async with aiofiles.open(self.filepath, mode="r", encoding="utf-8") as f:
                content = await f.read()

            lines = content.strip().split('\n')
            if len(lines) <= 1:
                return

            # Filter recent offers
            header = lines[0]
            recent_lines = [header]

            reader = csv.DictReader(lines)
            for row in reader:
                if row.get("date", "") >= cutoff_str:
                    # Reconstruct CSV line
                    line = ",".join(f'"{row.get(field, "")}"' for field in reader.fieldnames)
                    recent_lines.append(line)

            # Write back filtered content
            async with aiofiles.open(self.filepath, mode="w", encoding="utf-8") as f:
                await f.write("\n".join(recent_lines) + "\n")