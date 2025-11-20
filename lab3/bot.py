import asyncio
from aiogram import Dispatcher, Bot

from config import bot
from handlers import help, rate, recommend, start, stats


class TelegramBot:
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.dp = Dispatcher()

    def setup_routers(self) -> None:
        self.dp.include_router(start.router)
        self.dp.include_router(help.router)
        self.dp.include_router(rate.router)
        self.dp.include_router(recommend.router)
        self.dp.include_router(stats.router)

    async def run(self) -> None:
        self.setup_routers()
        await self.dp.start_polling(self.bot)


async def main() -> None:
    app = TelegramBot(bot)
    await app.run()


if __name__ == "__main__":
    print("Bot starting...")
    asyncio.run(main())
