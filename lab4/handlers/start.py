from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import ratings, MIN_RATINGS_FOR_CF
from service.get_user import get_or_create_user
from static import messages


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    Отправляет стартовое сообщение
    """
    internal = get_or_create_user(message.from_user.id)
    user_ratings = ratings.get(internal, {})
    if len(user_ratings) >= MIN_RATINGS_FOR_CF:
        await message.answer(messages.RECS_AVAILABLE)
    else:
        await message.answer(
            messages.START_TEXT.format(num=MIN_RATINGS_FOR_CF), parse_mode="HTML"
        )
