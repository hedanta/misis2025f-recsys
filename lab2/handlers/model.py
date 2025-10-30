from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from service.model_kb import get_model_keyboard
from static import messages
from service.state import set_user_model, get_user_model, MODELS

router = Router()


@router.message(F.text == "/model")
async def model_command(message: Message):
    """
    Сообщение с клавиатурой для выбора модели
    """
    model_name = get_user_model(message.from_user.id)
    await message.answer(
        messages.SELECT_MODEL.format(model_name=model_name),
        reply_markup=get_model_keyboard(),
    )


@router.callback_query(F.data.startswith("model:"))
async def on_model_selected(callback: CallbackQuery):
    user_id = callback.from_user.id
    model_key = callback.data.split(":", 1)[1]

    if model_key not in MODELS:
        await callback.answer(messages.UNKNOWN_MODEL)
        return

    set_user_model(user_id, model_key)
    model_name = MODELS[model_key]["name"]

    await callback.message.answer(
        messages.MODEL_SELECTED.format(model_name=model_name), parse_mode="HTML"
    )
