MODELS = {
    "gemma": {"id": "gemma3:4b", "name": "Gemma 3"},
    "llava": {"id": "llava-phi3", "name": "LLaVA Phi 3"},
}
DEFAULT_MODEL = "gemma"

_user_models = {}


def get_user_model(user_id: int) -> str:
    return _user_models.get(user_id, DEFAULT_MODEL)


def set_user_model(user_id: int, model_key: str):
    _user_models[user_id] = model_key
