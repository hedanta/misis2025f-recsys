import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TELEGRAM_TOKEN
from handlers import start, help, model, photo, text

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()
dp.include_router(start.router)
dp.include_router(help.router)
dp.include_router(model.router)
dp.include_router(photo.router)
dp.include_router(text.router)


async def main():
    bot = Bot(
        token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
