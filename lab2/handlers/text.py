from aiogram import Router, F
from aiogram.types import Message
from static import messages

router = Router()


@router.message(F.text)
async def handle_text(message: Message):
    """
    Срабатывает на текстовое сообщение без изображения
    """
    await message.answer(messages.TEXT_ONLY)
