"""Simplified application configuration without Pydantic."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    def __init__(self):
        # Discord settings
        self.discord_token = os.getenv("DISCORD_TOKEN")
        self.discord_channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))

        # Search settings
        self.search_location = os.getenv("SEARCH_LOCATION", "Siedlce")
        self.search_radius_km = int(os.getenv("SEARCH_RADIUS_KM", "150"))
        self.max_price = int(os.getenv("MAX_PRICE", "13000"))

        # Bot settings
        self.update_interval_seconds = int(os.getenv("UPDATE_INTERVAL_SECONDS", "900"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

        # Paths
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

    def get_otomoto_url(self) -> str:
        """Generate Otomoto search URL."""
        return (
            f"https://www.otomoto.pl/osobowe/{self.search_location.lower()}"
            f"?search%5Bdist%5D={self.search_radius_km}"
            f"&search%5Bfilter_float_price%3Ato%5D={self.max_price}"
            "&search%5Border%5D=created_at_first%3Adesc"
        )

    def get_lento_url(self) -> str:
        """Generate Lento search URL."""
        return (
            f"https://{self.search_location.lower()}.lento.pl/motoryzacja/samochody.html"
            f"?radius={int(self.search_radius_km / 3)}"
            f"&price_to={self.max_price}"
        )

    def get_autoplac_url(self) -> str:
        """Generate Autoplac search URL."""
        return (
            f"https://autoplac.pl/oferty/samochody-osobowe/mazowieckie/{self.search_location.lower()}"
            f"/cena-do-{int(self.max_price / 1000)}-tysiecy/prywatne"
            f"?range={self.search_radius_km}"
        )

    def get_sprzedajemy_url(self) -> str:
        """Generate Sprzedajemy search URL."""
        return (
            f"https://sprzedajemy.pl/{self.search_location.lower()}/motoryzacja/samochody-osobowe"
            f"?inp_distance={self.search_radius_km}"
            f"&inp_price%5Bto%5D={self.max_price}"
            "&offset=0&inp_seller_type_id=1"
        )


# Global settings instance
settings = Settings()