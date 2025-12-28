from config import ratings, tg_user_map
from config import TG_USER_MAP, RATINGS_JSON
from service.loader import save_json


def get_or_create_user(tg_id: int) -> str:
    key = str(tg_id)
    if key in tg_user_map:
        return tg_user_map[key]

    internal = f"tg_{tg_id}"
    tg_user_map[key] = internal

    save_json(TG_USER_MAP, tg_user_map)

    # добавляем пользователя в общий словарь оценок
    if internal not in ratings:
        ratings[internal] = {}
        save_json(RATINGS_JSON, ratings)
    return internal
