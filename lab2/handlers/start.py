from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from static import messages
from service.model_kb import get_model_keyboard
from service.state import set_user_model, get_user_model, MODELS, DEFAULT_MODEL

router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    set_user_model(user_id, DEFAULT_MODEL)
    model = MODELS[get_user_model(user_id)]

    await message.answer(
        messages.START_TEXT.format(model_name=model["name"]),
        parse_mode="HTML",
        reply_markup=get_model_keyboard(),
    )
