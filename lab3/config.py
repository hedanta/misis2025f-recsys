from dotenv import load_dotenv
import os
from aiogram import Dispatcher, Bot
from service.loader import load_anime_df, load_json
from pathlib import Path
from typing import Dict

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DATA_DIR = os.getenv("DATA_DIR")

MIN_RATINGS_FOR_CF = int(os.getenv("MIN_RATINGS_FOR_CF", "10"))
NEIGHBORS = int(os.getenv("NEIGHBORS", "15"))
TOP_K = int(os.getenv("TOP_K", "5"))
RANDOM_CANDIDATES = int(os.getenv("RANDOM_CANDIDATES", "100"))

ANIME_CSV = Path(DATA_DIR + "/anime.csv")
RATINGS_JSON = Path(DATA_DIR + "/ratings.json")
TG_USER_MAP = Path(DATA_DIR + "/tg_user_map.json")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

anime_df = load_anime_df(ANIME_CSV)
sorted_df = anime_df.sort_values("members", ascending=False)
ratings: Dict[str, Dict[str, float]] = load_json(RATINGS_JSON)
tg_user_map: Dict[str, str] = load_json(TG_USER_MAP)
