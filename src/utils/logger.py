"""Logging utilities."""
import logging
import sys
from pathlib import Path
from datetime import datetime
import discord

from src.config.settings import settings


def setup_logging() -> None:
    """Setup application logging."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    # Setup file handler
    log_file = log_dir / f"bot_{datetime.now():%Y%m%d}.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(getattr(logging, settings.log_level))

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Reduce noise from libraries
    logging.getLogger("discord").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)


class DiscordLogger:
    """Logger that sends messages to Discord channel."""

    def __init__(self, channel: discord.TextChannel):
        """Initialize Discord logger."""
        self.channel = channel
        self.logger = logging.getLogger(__name__)

    async def log(self, message: str, emoji: str = "🪵") -> None:
        """Send log message to Discord channel."""
        try:
            await self.channel.send(f"{emoji} {message}")
            self.logger.info(f"Discord log: {message}")
        except Exception as e:
            self.logger.error(f"Failed to send Discord log: {e}")