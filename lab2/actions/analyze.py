import aiohttp
import asyncio
import logging
from static import messages
from config import OLLAMA_URL

API_URL = OLLAMA_URL


async def analyze_image(prompt: str, model_id: str, image_bytes: bytes) -> str:
    """
    Отправляет запрос к Ollama API и возвращает текстовый ответ модели

    :param prompt: Текстовый запрос к модели
    :param model_id: id выбранной модели
    :image_bytes: Изображение в base64 формате

    :return Строка с ответом модели
    """
    async with aiohttp.ClientSession() as session:
        form = aiohttp.FormData()
        form.add_field("model", model_id)
        form.add_field("prompt", prompt)
        form.add_field(
            "file", image_bytes, filename="image.png", content_type="image/png"
        )

        try:
            async with session.post(
                f"{API_URL}/analyze", data=form, timeout=30
            ) as resp:
                try:
                    data = await resp.json()
                except aiohttp.ContentTypeError:
                    text = await resp.text()
                    logging.error(f"Error decoding API answer: {text}")

                if resp.status != 200 or data.get("status") != "success":
                    error_detail = (
                        data.get("detail") or data.get("message") or "API error"
                    )
                    logging.error(f"API error: {error_detail}")
                    return messages.ERROR_API(detail=error_detail)

                return data["data"]["response"]

        except asyncio.TimeoutError:
            logging.error("Timeout error while waiting for the server response.")
            return messages.ERROR_API.format(
                detail="Превышено время ожидания ответа сервера."
            )

        except aiohttp.ClientConnectionError:
            logging.error("Failed to connect to the API server.")
            return messages.ERROR_API.format(
                detail="Не удалось подключиться к серверу API."
            )

        except aiohttp.ClientError as e:
            logging.error(f"HTTP ClientError: {type(e).__name__} - {e}")
            return messages.ERROR_API.format(detail="Ошибка при обработке запроса.")

        except Exception as e:
            logging.exception("Unexpected error during image analysis")
            return messages.ERROR_ANALYSIS
