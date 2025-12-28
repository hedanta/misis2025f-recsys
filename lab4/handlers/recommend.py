from aiogram import Router, F
from aiogram.types import Message

from svdpp.recommender import recommend_for_user
from config import ratings, watched, anime_df, TOP_K, svdpp_model
from service.get_user import get_or_create_user
from service.get_random import send_for_rating
from static import messages

router = Router()


@router.message(F.text == "/rec")
async def cmd_rec_svd(message: Message):
    """
    Отправляет список рекомендованных аниме.
    Если оценок недостаточно, предлагает оценить ещё.
    """
    user = get_or_create_user(message.from_user.id)
    print(user)

    if len(ratings.get(user, {})) < 0:
        await message.answer(messages.FEW_SCORED.format(num=3))
        return await send_for_rating(message.chat.id)

    recs = recommend_for_user(svdpp_model, user, TOP_K)

    if not recs:
        await message.answer(messages.NO_RECS)
        return await send_for_rating(message.chat.id)

    text_lines = messages.RECS.copy()
    for aid in recs:
        row = anime_df.loc[anime_df["anime_id"].astype(str) == str(aid)]
        if not row.empty:
            text_lines.append(row["title_english"].iloc[0])

    await message.answer("\n".join(text_lines))
