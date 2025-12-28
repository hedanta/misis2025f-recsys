from dotenv import load_dotenv
import os
from aiogram import Dispatcher, Bot
from service.loader import load_anime_df, load_json
from svdpp.svdpp import SVDPlusPlus
from models.models import UserRatings, Watched
from pathlib import Path
from typing import Dict


load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DATA_DIR = os.getenv("DATA_DIR")

MIN_RATINGS_FOR_CF = int(os.getenv("MIN_RATINGS_FOR_CF", "3"))
TOP_K = int(os.getenv("TOP_K", "5"))
RANDOM_CANDIDATES = int(os.getenv("RANDOM_CANDIDATES", "100"))

MODEL_PATH = Path("svdpp.pkl")
ANIME_CSV = Path(DATA_DIR + "/anime.csv")
RATINGS_JSON = Path(DATA_DIR + "/ratings.json")
WATCHED_JSON = Path(DATA_DIR + "/watched.json")
TG_USER_MAP = Path(DATA_DIR + "/tg_user_map.json")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

anime_df = load_anime_df(ANIME_CSV)
sorted_df = anime_df.sort_values("members", ascending=False)
ratings: UserRatings = load_json(RATINGS_JSON)
watched_raw = load_json(WATCHED_JSON)
watched = {u: set(items) for u, items in watched_raw.items()}
tg_user_map: Dict[str, str] = load_json(TG_USER_MAP)


if MODEL_PATH.exists():
    svdpp_model = SVDPlusPlus.load(MODEL_PATH)
else:
    svdpp_model = SVDPlusPlus(factors=20, epochs=5)
    svdpp_model.fit(ratings, watched)
    svdpp_model.save(MODEL_PATH)
