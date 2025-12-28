import asyncio
import logging
from aiogram import Dispatcher, Bot

from config import bot
from handlers import help, rate, recommend, start, stats


class TelegramBot:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.dp = Dispatcher()

        self._setup_logging()

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging initialized")

    def setup_routers(self) -> None:
        self.dp.include_router(start.router)
        self.dp.include_router(help.router)
        self.dp.include_router(rate.router)
        self.dp.include_router(recommend.router)
        self.dp.include_router(stats.router)
        self.logger.info("Routers registered")

    async def run(self) -> None:
        self.setup_routers()
        await self.dp.start_polling(self.bot)
        self.logger.info("Bot started polling")


async def main() -> None:
    app = TelegramBot(bot)
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
