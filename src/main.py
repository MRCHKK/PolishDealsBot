"""Main entry point for the car offers bot."""
import asyncio
import logging
import signal
import sys
from typing import Optional

from src.bot.client import OfferBot
from src.bot.handlers import OfferHandler
from src.config.settings import settings
from src.utils.logger import setup_logging


class Application:
    """Main application class."""

    def __init__(self):
        """Initialize application."""
        self.bot: Optional[OfferBot] = None
        self.handler: Optional[OfferHandler] = None
        self.logger = logging.getLogger(__name__)

    async def start(self) -> None:
        """Start the application."""
        self.logger.info("Starting Car Offers Bot...")

        # Create bot and handler
        self.bot = OfferBot()
        self.handler = OfferHandler(self.bot)

        # Setup event listeners
        @self.bot.event
        async def on_bot_initialized(channel):
            """Handle bot initialization."""
            await self.handler.initialize(channel)

        # Start bot
        await self.bot.start(settings.discord_token)

    async def shutdown(self) -> None:
        """Gracefully shutdown the application."""
        self.logger.info("Shutting down...")

        if self.handler:
            self.handler.stop()

        if self.bot:
            await self.bot.close()

        # Wait for pending tasks
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        if tasks:
            self.logger.info(f"Cancelling {len(tasks)} pending tasks...")
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

        self.logger.info("Shutdown complete")

    def setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown."""
        def signal_handler(sig, frame):
            self.logger.info(f"Received signal {sig}")
            asyncio.create_task(self.shutdown())

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)


async def main():
    """Main function."""
    # Setup logging
    setup_logging()

    # Create and run application
    app = Application()
    app.setup_signal_handlers()

    try:
        await app.start()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
    finally:
        await app.shutdown()


if __name__ == "__main__":
    # Windows-specific event loop policy
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Run the bot
    asyncio.run(main())