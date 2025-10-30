from io import BytesIO
from aiogram import Router, F
from aiogram.types import Message
from static import messages, prompts
from actions.analyze import analyze_image
from service.state import get_user_model, MODELS

router = Router()


@router.message(F.photo)
async def handle_photo(message: Message):
    """
    Срабатывает на сообщение с изображением, отправляет на анализ и возвращает ответ модели
    """
    user_id = message.from_user.id
    model_key = get_user_model(user_id)
    model = MODELS[model_key]

    caption = (message.caption or prompts.BASIC_PROMPT).strip()
    await message.answer(
        messages.ANALYZING.format(model_name=model["name"]), parse_mode="HTML"
    )

    bot = message.bot
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)

    photo_bytes = BytesIO()
    await bot.download_file(file.file_path, destination=photo_bytes)
    photo_bytes.seek(0)

    result = await analyze_image(caption, model["id"], photo_bytes.getvalue())
    await message.reply(result)
