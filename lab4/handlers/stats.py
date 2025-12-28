from aiogram import F, Router
from aiogram.types import Message

from config import anime_df, ratings, watched
from service.get_user import get_or_create_user
from static import messages

router = Router()


@router.message(F.text == "/stats")
async def cmd_stats(message: Message):
    """
    Отправляет список текущих оценок и просмотренных аниме пользователя
    """
    user = get_or_create_user(message.from_user.id)
    scored = ratings.get(user, {})
    seen = watched.get(user, set())

    if not scored and not seen:
        return await message.answer(messages.NO_SAVED_SCORES)

    lines = []

    # оценённые
    if scored:
        lines.append(messages.STATS)
        for aid, score in scored.items():
            row = anime_df.loc[anime_df["anime_id"].astype(str) == str(aid)]
            if row.empty:
                continue
            title = row["title_english"].iloc[0]
            lines.append(f"{title}: {score}")

    # просмотренные без оценки
    unseen_scored = seen - set(scored.keys())
    if unseen_scored:
        # lines.append(messages.WATCHED)
        for aid in unseen_scored:
            row = anime_df.loc[anime_df["anime_id"].astype(str) == str(aid)]
            if row.empty:
                continue
            title = row["title_english"].iloc[0]
            lines.append(title)

    await message.answer("\n".join(lines))
