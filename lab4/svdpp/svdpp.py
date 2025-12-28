import math
import pickle
import logging
from typing import Dict, List, Tuple
from models.models import UserRatings, Watched

import numpy as np

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SVDPlusPlus:
    """
    Реализация меотда SVD++

    Модель разложения матрицы рейтингов с учетом
    implicit feedback (в л/р просмотры и оценки)

    Обучение производится методом стохастического
    градиентного спуска
    """

    def __init__(
        self,
        factors: int = 20,
        lr: float = 0.01,
        reg: float = 0.02,
        epochs: int = 20,
        seed: int = 42,
    ) -> None:
        """
        Инициализирует модель

        :param factors: размерность латентного пространства
        :param lr: скорость обучения
        :param reg: коэффициент регуляризации
        :param epochs: число эпох обучения
        :param seed: сид генератора случайных чисел
        """
        np.random.seed(seed)

        self.k: int = factors
        self.lr: float = lr
        self.reg: float = reg
        self.epochs: int = epochs

        # глобальное среднее рейтингов
        self.mu: float = 0.0

        # Словари id-индекс
        self.user_to_index: Dict[str, int] = {}
        self.item_to_index: Dict[str, int] = {}

        # latent-факторы
        self.pu: np.ndarray = None
        self.qi: np.ndarray = None
        self.yi: np.ndarray = None

        self.bu: np.ndarray = None
        self.bi: np.ndarray = None

        # списки просмотренных объектов для каждого пользователя
        self.user_items_list: List[List[int]] = []

    def _init_matrix(self, rows: int) -> np.ndarray:
        """
        Инициализирует латентную матрицу случайными значениями.

        Каждая строка соответствует пользователю или объекту, 
        каждая колонка — латентному фактору.
        Значения выбираются равномерно из диапазона [-0.1, 0.1].

        :param rows: количество строк в матрице
        :return: матрица с начальными латентными факторами
        """
        return np.random.uniform(-0.1, 0.1, (rows, self.k))

    def _implicit_sum(self, user: str) -> np.ndarray:
        """
        Вычисляет сумму implicit факторов для пользователя:

        sum_{j in N(u)} y_j / sqrt(|N(u)|)

        :param user: ID пользователя
        :returns: вектор implicit факторов
        """
        Nu = self.user_items_list[user]
        if not Nu:
            return np.zeros(self.k, dtype=float)
        return np.sum(self.yi[Nu, :], axis=0) / math.sqrt(len(Nu))

    def add_user(self, user: str) -> int:
        """
        Добавляет нового пользователя в модель.

        :param user: ID пользователя
        :returns: индекс пользователя в массивах модели
        """
        u_idx = len(self.user_to_index)
        self.user_to_index[user] = u_idx

        self.pu = np.vstack([self.pu, self._init_matrix(1)])
        self.bu = np.append(self.bu, 0.0)

        self.user_items_list.append([])

        logger.info(f"added user: {user}")
        return u_idx

    def add_watched(self, user: str, item: str) -> None:
        """
        Добавляет объект в список implicit факторов

        :param user: ID пользователя
        :param item: объект
        """
        logging.info(f"add_watched called: user={user}, item={item}")

        if user not in self.user_to_index:
            logging.warning(f"user {user} NOT in model")
            return

        u_idx = self.user_to_index[user]
        i_idx = self.item_to_index[item]

        if i_idx not in self.user_items_list[u_idx]:
            self.user_items_list[u_idx].append(i_idx)
            logging.info(f"implicit item {item} added")
        else:
            logging.info(f"implicit item {item} already exists")

    def predict(self, user: str, item: str) -> float:
        """
        Считает предсказание рейтинга пользователя для объекта.

        :param user: ID пользователя
        :param item: объект
        :returns: предсказанный рейтинг
        """
        if user not in self.user_to_index or item not in self.item_to_index:
            # возвращаем среднее
            return self.mu

        u_idx = self.user_to_index[user]
        i_idx = self.item_to_index[item]
        y_sum = self._implicit_sum(u_idx)

        return (
            self.mu
            + self.bu[u_idx]
            + self.bi[i_idx]
            + np.dot(self.qi[i_idx], self.pu[u_idx] + y_sum)
        )

    def fit_one(self, user: str, item: str, rating: float) -> float:
        """
        Производит один шаг SGD

        :param user: ID пользователя
        :param item: объект
        :param rating: оценка объекта пользователем
        :returns: ошибку предсказания (rating - predict)
        """
        if user not in self.user_to_index:
            return

        u_idx = self.user_to_index[user]
        i_idx = self.item_to_index[item]

        y_sum = self._implicit_sum(u_idx)
        pred = (
            self.mu
            + self.bu[u_idx]
            + self.bi[i_idx]
            + np.dot(self.qi[i_idx], self.pu[u_idx] + y_sum)
        )
        err = rating - pred

        # обновление bias
        self.bu[u_idx] += self.lr * (err - self.reg * self.bu[u_idx])
        self.bi[i_idx] += self.lr * (err - self.reg * self.bi[i_idx])

        pu_old = self.pu[u_idx].copy()
        qi_old = self.qi[i_idx].copy()

        # обновление латентных матриц
        self.pu[u_idx] += self.lr * (err * qi_old - self.reg * pu_old)
        self.qi[i_idx] += self.lr * (err * (pu_old + y_sum) - self.reg * qi_old)

        # обновление implicit
        Nu = self.user_items_list[u_idx]
        if Nu:
            scale = 1.0 / math.sqrt(len(Nu))
            self.yi[Nu, :] += self.lr * (
                err * qi_old * scale - self.reg * self.yi[Nu, :]
            )

        return err

    def fit(self, ratings: UserRatings, watched: Watched) -> None:
        """
        Обучение модели на полном датасете.

        :param ratings: словарь оценок пользователями
        :param watched: список просмотренных без оценки (implicit feedback)
        """
        logging.info("Training started")

        users = list(ratings.keys())
        items = list(
            {i for user_ratings in ratings.values() for i in user_ratings.keys()}
        )
        num_users = len(users)
        num_items = len(items)

        # id-index
        self.user_to_index = {u: idx for idx, u in enumerate(users)}
        self.item_to_index = {i: idx for idx, i in enumerate(items)}

        # инициализируем латентные матрицы
        self.pu = self._init_matrix(num_users)
        self.qi = self._init_matrix(num_items)
        self.yi = self._init_matrix(num_items)

        self.bu = np.zeros(num_users, dtype=float)
        self.bi = np.zeros(num_items, dtype=float)

        self.user_items_list = []
        data: List[Tuple[int, int, float]] = []

        for u_idx, u in enumerate(users):
            rated_items = ratings[u]
            watched_items = watched.get(u, set())
            implicit = list(rated_items.keys())
            for i in watched_items:
                if i not in rated_items:
                    implicit.append(i)

            implicit_idx = [self.item_to_index[i] for i in implicit]
            self.user_items_list.append(implicit_idx)

            for i, r in rated_items.items():
                data.append((u_idx, self.item_to_index[i], r))

        self.mu = float(np.mean([r for _, _, r in data]))

        # обучение
        for epoch in range(1, self.epochs + 1):
            np.random.shuffle(data)
            sq_err = 0.0
            for u_idx, i_idx, r in data:
                err = self.fit_one(users[u_idx], items[i_idx], r)
                sq_err += err * err
            rmse = math.sqrt(sq_err / len(data))
            logger.info(f"Epoch {epoch}/{self.epochs} | RMSE: {rmse:.4f}")

    def save(self, path: str) -> None:
        """
        Сохраняет обученную модель

        :param path: путь к файлу
        """
        with open(path, "wb") as f:
            pickle.dump(self, f)
            logging.info("Saved model")

    def load(path: str) -> "SVDPlusPlus":
        """
        Загружает модель
        
        :param path: путь к файлу
        :returns: SVD++ модель
        """
        with open(path, "rb") as f:
            logging.info("Loaded model")
            return pickle.load(f)
