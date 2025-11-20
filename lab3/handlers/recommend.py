from aiogram import F, Router
from aiogram.types import Message

from cf.recommender import recommend_for_user
from config import anime_df, ratings
from config import MIN_RATINGS_FOR_CF, TOP_K
from service.get_random import send_for_rating
from service.get_user import get_or_create_user
from static import messages

router = Router()


@router.message(F.text == "/rec")
async def cmd_recommend(message: Message):
    """
    Отправляет список рекомендованных аниме.
    Если оценок недостаточно, предлагает оценить ещё.
    """
    user = get_or_create_user(message.from_user.id)

    # недостаточно оценок
    if len(ratings.get(user, {})) < MIN_RATINGS_FOR_CF:
        await message.answer(messages.FEW_SCORED.format(num=MIN_RATINGS_FOR_CF))
        return await send_for_rating(message.chat.id)

    recs = recommend_for_user(user, ratings, TOP_K)

    # по текущим оценкам нет рекомендаций
    if not recs:
        await message.answer(messages.NO_RECS)
        return await send_for_rating(message.chat.id)

    # формируем список рекомендаций
    text_lines = messages.RECS.copy()
    for aid in recs:
        row = anime_df.loc[anime_df["anime_id"].astype(str) == str(aid)]
        if row.empty:
            continue
        title = row["title_english"].iloc[0]
        text_lines.append(title)

    await message.answer("\n".join(text_lines))
