import os

from dotenv import load_dotenv


def get_allowed_origins():
    load_dotenv()

    origins = os.environ.get("ALLOWED_ORIGINS", None)

    if origins is None:
        return []

    return origins.split(",")