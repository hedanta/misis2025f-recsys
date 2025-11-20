import math
from typing import Dict, Optional


def pearson_corr(
    u_ratings: Dict[str, float], v_ratings: Dict[str, float]
) -> Optional[float]:
    """
    Считает коэффициент Пирсона между двумя пользователями по оценкам обших аниме.
    :param u_ratings Словарь оценок первого пользователя
    :param v_ratings Словарь оценок второго пользователя

    :return Коэффициент корреляции Пирсона (None если пересечений < 2 или дисперсия нулевая)
    """
    common = set(u_ratings.keys()) & set(v_ratings.keys())
    n = len(common)
    if n < 2:
        return None

    u_vals = [u_ratings[a] for a in common]
    v_vals = [v_ratings[a] for a in common]

    mean_u = sum(u_vals) / n
    mean_v = sum(v_vals) / n

    num = sum((u_vals[i] - mean_u) * (v_vals[i] - mean_v) for i in range(n))
    den_u = math.sqrt(sum((u_vals[i] - mean_u) ** 2 for i in range(n)))
    den_v = math.sqrt(sum((v_vals[i] - mean_v) ** 2 for i in range(n)))
    denom = den_u * den_v

    if denom == 0:
        return None
    return num / denom
