import pandas as pd
from typing import List

from cf.pearson import pearson_corr
from models.models import UserRatings


def recommend_for_user(
    target: str,
    ratings: UserRatings,
    top_neighbors: int = 15,
    top_k: int = 5,
) -> List[str]:
    """
    Формирует рекомендации для пользователей с помощью user-based CF

    :param target ID текущего пользователя
    :param ratings Словарь с оценками всех пользователей вида {user_id: {anime_id: score}}
    :param top_neighbors Количество учитывающихся наиболее похожих пользователей
    :param top_k Количество возвращаемых рекомендаций

    :return Список anime_id длиной до top_k, отсортированных по убыванию предсказаний
    """
    if target not in ratings:
        return []

    u_r = ratings[target]
    seen = set(u_r.keys())

    # похожие пользователи
    sims = []
    for other, r in ratings.items():
        if other == target:
            continue
        corr = pearson_corr(u_r, r)
        if corr is not None and corr > 0:
            sims.append((other, corr))

    if not sims:
        return []

    sims.sort(key=lambda x: x[1], reverse=True)
    neighbors = sims[:top_neighbors]

    # агрегированные веса
    scores = {}
    for uid, weight in neighbors:
        for aid, score in ratings[uid].items():
            if aid in seen:
                continue
            scores.setdefault(aid, 0.0)
            scores[aid] += weight * score

    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

    return [aid for aid, _ in top]
