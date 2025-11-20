from aiogram import F, Router
from aiogram.types import Message

from config import anime_df, ratings
from service.get_user import get_or_create_user
from static import messages

router = Router()


@router.message(F.text == "/stats")
async def cmd_stats(message: Message):
    """
    Отправляет список текущих оценок пользователя
    """
    user = get_or_create_user(message.from_user.id)
    scored = ratings.get(user, {})

    if not scored:
        await message.answer(messages.NO_SAVED_SCORES)
        return

    titles = {}
    for aid, score in scored.items():
        row = anime_df.loc[anime_df["anime_id"].astype(str) == str(aid)]
        title = row["title_english"].iloc[0]
        titles[title] = score
    lines = [f"{anime}: {score}" for anime, score in titles.items()]
    text = messages.SCORES + "\n".join(lines)

    await message.answer(text)
