import os
from dotenv import load_dotenv

load_dotenv()


def _get_or_exception(key):
    value = os.getenv(key)
    if value is None:
        raise TypeError(f"Environment variable '{key}' does not exist!")
    return value


PATH_MODEL = _get_or_exception("PRODUCTION_MODEL_PATH")
PATH_TRAINING_DATA = _get_or_exception("PRODUCTION_TRAIN_DATA_PATH")
