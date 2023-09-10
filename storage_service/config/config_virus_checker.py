from dotenv import load_dotenv

import os


def get_virus_checker_api_key():
    load_dotenv()

    return {
        "api_key": os.environ.get("VIRUS_CHECKER_API_KEY")
    }
