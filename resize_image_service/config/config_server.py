from dotenv import load_dotenv

import os


def get_config_server():
    load_dotenv()
    return {
        "host": os.environ.get("SERVER_HOST", "0.0.0.0"),
        "port": os.environ.get("SERVER_PORT", 8000),
    }
