from typing import List
from svdpp.svdpp import SVDPlusPlus


def recommend_for_user(
    model: SVDPlusPlus,
    user: str,
    top_k: int = 5,
) -> List[str]:
    """
    Рекомендации с помощью SVD++

    :param model: модель рекомендаций
    :param user: ID пользователя
    :param top_k: количество возвращаемых рекомендаций
    :returns: список из k рекомендаций
    """
    if user not in model.user_to_index:
        return []

    u_idx = model.user_to_index[user]

    seen_idx = set(model.user_items_list[u_idx])
    seen_items = {item for item, idx in model.item_to_index.items() if idx in seen_idx}

    items = [item for item in model.item_to_index if item not in seen_items]

    top = [(i, model.predict(user, i)) for i in items]
    top.sort(key=lambda x: x[1], reverse=True)

    return [i for i, _ in top[:top_k]]
