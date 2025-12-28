from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def rating_keyboard(anime_id: str) -> InlineKeyboardMarkup:
    # кнопки от 1 до 10 в два столбца
    buttons = []
    for s in range(1, 11, 2):
        row = [
            InlineKeyboardButton(text=str(s), callback_data=f"rate|{anime_id}|{s}"),
            InlineKeyboardButton(
                text=str(s + 1), callback_data=f"rate|{anime_id}|{s + 1}"
            ),
        ]
        buttons.append(row)

    # кнопки просмотра и пропуска отдельной строкой
    buttons.append(
        [
            InlineKeyboardButton(
                text="Просмотрено", callback_data=f"watched|{anime_id}"
            ),
            InlineKeyboardButton(text="Пропустить", callback_data=f"skip|{anime_id}"),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
