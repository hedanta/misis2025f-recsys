import random

from config import sorted_df, bot
from config import RANDOM_CANDIDATES
from service.rating_kb import rating_keyboard
from static import messages


async def send_for_rating(chat_id: int):
    """
    Отправляет случайные аниме для оценки из топ-N самых популярных
    """
    pool = list(sorted_df["anime_id"].values[:500])

    # случайная выборка
    to_show = random.sample(pool, min(1, len(pool)))

    for aid in to_show:
        row = sorted_df[sorted_df["anime_id"] == aid]
        title = row["title_english"].iloc[0]
        await bot.send_message(
            chat_id,
            messages.FOR_RATE.format(title=title),
            reply_markup=rating_keyboard(str(aid)),
        )
