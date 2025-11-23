import pandas as pd
from typing import List

from cf.pearson import pearson_corr
from models.models import UserRatings


from typing import Dict, Optional, List, Tuple


def predict(
    target_r: Dict[str, float],
    item: str,
    neighbors: List[Tuple[str, float]],
    ratings: UserRatings,
) -> Optional[float]:
    """
    Вычисляет предсказанный рейтинг пользователя для заданного объекта
    на основе user-based CF по формуле:
    r = target_mean + sum(sim(u, v) * (r_vi - mean_v)) / sum(|sim(u, v)|)

    :param target_r: Оценки целевого пользователя
    :param item: ID объекта, для которого вычисляется предсказание
    :param neighbors: Список соседей вида (user_id, similarity), отсортированный по похожести
    :param ratings: Словарь с оценками всех пользователей вида {user_id: {anime_id: score}}

    :return: Предсказанный рейтинг или None, если предсказание невозможно
    """
    target_mean = sum(target_r.values()) / len(target_r)

    num = 0.0
    den = 0.0

    for user_id, sim in neighbors:
        r_v = ratings[user_id]

        if item not in r_v:
            continue

        mean_v = sum(r_v.values()) / len(r_v)

        num += sim * (r_v[item] - mean_v)
        den += abs(sim)

    return target_mean + num / den if den else None


def recommend_for_user(
    target: str,
    ratings: UserRatings,
    top_neighbors: int = 15,
    top_k: int = 5,
) -> List[str]:
    """
    Формирует рекомендации для пользователей с помощью user-based CF

    :param target: ID текущего пользователя
    :param ratings: Словарь с оценками всех пользователей вида {user_id: {anime_id: score}}
    :param top_neighbors: Количество учитывающихся наиболее похожих пользователей
    :param top_k: Количество возвращаемых рекомендаций

    :return: Список anime_id длиной до top_k, отсортированных по убыванию предсказаний
    """
    if target not in ratings:
        return []

    target_r = ratings[target]
    seen = set(target_r)

    sims = []
    for user_id, scores in ratings.items():
        if user_id == target:
            continue
        sim = pearson_corr(target_r, scores)
        if sim:
            sims.append((user_id, sim))

    if not sims:
        return []

    sims.sort(key=lambda x: abs(x[1]), reverse=True)
    neighbors = sims[:top_neighbors]

    items = set()

    for user_ratings in ratings.values():
        for anime_id in user_ratings:
            if anime_id not in seen:
                items.add(anime_id)

    preds = {}

    for item in items:
        pred = predict(target_r, item, neighbors, ratings)
        if pred is not None:
            preds[item] = pred

    top = sorted(preds.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return [anime_id for anime_id, _ in top]
