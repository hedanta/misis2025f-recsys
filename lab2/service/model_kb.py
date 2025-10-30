from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from service.state import MODELS


def get_model_keyboard():
    buttons = [
        [InlineKeyboardButton(text=info["name"], callback_data=f"model:{key}")]
        for key, info in MODELS.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
