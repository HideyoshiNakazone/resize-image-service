from dotenv import load_dotenv

import os


def get_config_redis():
    load_dotenv()
    return {
        "host": os.environ.get("REDIS_HOST", "localhost"),
        "port": os.environ.get("REDIS_PORT", 6379),
        "password": os.environ.get("REDIS_PASSWORD", None),
    }
