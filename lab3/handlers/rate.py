from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from config import MIN_RATINGS_FOR_CF, RATINGS_JSON
from config import ratings, bot
from service.get_user import get_or_create_user
from service.get_random import send_for_rating
from service.loader import save_json
from static import callback_msg
from static import messages


router = Router()


@router.message(F.text == "/rate")
async def cmd_rate(message: Message):
    """
    Отправляет аниме для оценки и сохраняет результат.
    Аниме предлагаются до тех пор, пока не будет набрано
    минимально необходимое количество оценок
    """
    use = get_or_create_user(message.from_user.id)
    await send_for_rating(message.chat.id)


@router.callback_query(
    lambda c: c.data and (c.data.startswith("rate|") or c.data.startswith("skip|"))
)
async def process_rating_callback(callback: CallbackQuery):
    data = callback.data.split("|")
    action = data[0]
    anime_id = data[1]
    user = get_or_create_user(callback.from_user.id)

    if action == "skip":
        await callback.answer(callback_msg.SKIPPED)
        return await send_for_rating(callback.message.chat.id)

    score = float(data[2])

    if user not in ratings:
        ratings[user] = {}

    ratings[user][str(anime_id)] = score

    save_json(RATINGS_JSON, ratings)

    await callback.answer(callback_msg.SAVED.format(score=score))
    await bot.send_message(
        callback.message.chat.id, messages.SAVED_SCORE.format(score=score)
    )

    # недостаточно оценок для рекомендаций
    if len(ratings.get(user, {})) < MIN_RATINGS_FOR_CF:
        await send_for_rating(callback.message.chat.id)
