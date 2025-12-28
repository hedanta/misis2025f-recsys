import json
import pandas as pd
from pathlib import Path
from typing import Dict


def load_anime_df(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def load_json(path: Path) -> Dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_json(path: Path, obj: Dict):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
