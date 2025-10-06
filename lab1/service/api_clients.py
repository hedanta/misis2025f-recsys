import requests
import logging
from typing import Dict, List, Optional, Any

logging.basicConfig(level=logging.INFO)


class TagAPIClient:
    """Базовый класс клиентов с rapidapi"""

    def __init__(self, api_url: str, api_key: str, api_host: str):
        self.api_url = api_url
        self.headers = {
            "x-rapidapi-host": api_host,
            "x-rapidapi-key": api_key,
            "Content-Type": "application/json",
        }

    def _post(self, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Функция для выполнения POST-запроса к API и возврата JSON-ответа

        :param payload: данные для запроса
        :return: словарь с тегами
        """
        try:
            r = requests.post(self.api_url, headers=self.headers, json=payload)
            r.raise_for_status()
            return r.json()
        except requests.Timeout:
            logging.error("%s request timeout", self.__class__.__name__)
        except requests.HTTPError as e:
            logging.error("%s HTTP error: %s", self.__class__.__name__, e)
        except requests.RequestException as e:
            logging.error("%s error: %s", self.__class__.__name__, e)
        return None


class KiraAPIClient(TagAPIClient):

    def get_tags(self, image_url: str) -> List[str]:
        """
        Возвращает отсортированный список тегов для изображения

        :param image_url: URL изображения
        :return: список тегов, отсортированный по алфавиту
        """
        data = self._post({"imageUrl": image_url})
        if data is None:
            return []

        tags = [t["name"] for t in data.get("tags", []) if "name" in t]
        logging.info("KiraAPI returned %d tags", len(tags))
        return sorted(tags)


class OdlicaAPIClient(TagAPIClient):

    def get_tags(
        self, image_url: str, min_count: int = 1, max_count: int = 20
    ) -> List[str]:
        """
        Возвращает отсортированный список тегов для изображения

        :param input_image: URL изображения
        :param input_type: тип изображения (url/base64)
        :param min_keywords_count: мин. количество тегов
        :param max_keywords_count: макс. количество тегов
        :return: список тегов, отсортированный по алфавиту
        """
        payload = {
            "input_image": image_url,
            "input_type": "url",
            "min_keywords_count": min_count,
            "max_keywords_count": max_count,
        }
        data = self._post(payload)
        if data is None:
            return []

        tags = data.get("data", {}).get("keywords", [])
        if not isinstance(tags, list):
            return []

        logging.info("OdlicaAPI returned %d tags", len(tags))
        return sorted(tags)
