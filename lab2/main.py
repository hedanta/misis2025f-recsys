import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TELEGRAM_TOKEN
from handlers import start, help, model, photo, text


class TelegramApp:
    def __init__(self, token: str):
        self.token = token
        self.bot = Bot(
            token=self.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        self.dp = Dispatcher()
        self._setup_logging()
        self._register_routers()

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logging initialized")

    def _register_routers(self):
        self.dp.include_router(start.router)
        self.dp.include_router(help.router)
        self.dp.include_router(model.router)
        self.dp.include_router(photo.router)
        self.dp.include_router(text.router)
        self.logger.info("Routers registered")

    async def start(self):
        self.logger.info("Starting bot polling...")
        await self.dp.start_polling(self.bot)


async def main():
    app = TelegramApp(TELEGRAM_TOKEN)
    await app.start()


if __name__ == "__main__":
    asyncio.run(main())
