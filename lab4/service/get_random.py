import random
from config import sorted_df, bot, RANDOM_CANDIDATES, ratings, watched
from service.rating_kb import rating_keyboard
from static import messages


async def send_for_rating(chat_id: int, user_id: str):
    """
    Отправляет случайное аниме для оценки из топ-N популярных,
    которое пользователь ещё не видел и не оценил.
    """
    seen = set(ratings.get(user_id, {}).keys()) | watched.get(user_id, set())
    pool = [
        aid
        for aid in sorted_df["anime_id"].values[:RANDOM_CANDIDATES]
        if aid not in seen
    ]

    aid = random.choice(pool)
    row = sorted_df[sorted_df["anime_id"] == aid]
    title = row["title_english"].iloc[0]

    await bot.send_message(
        chat_id,
        messages.FOR_RATE.format(title=title),
        reply_markup=rating_keyboard(str(aid)),
    )
