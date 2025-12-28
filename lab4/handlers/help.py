from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from static import messages

router = Router()


@router.message(Command("help"))
async def help_handler(message: Message):
    """
    Отправляет справку по боту
    """
    await message.answer(messages.HELP_TEXT, parse_mode="HTML")
