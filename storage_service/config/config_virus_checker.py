from dotenv import load_dotenv

import os


def get_virus_checker_api_key() -> str:
    load_dotenv()

    api_key = os.environ.get("VIRUS_CHECKER_API_KEY")

    if not api_key:
        raise RuntimeError("Virus Checker API Key not found")

    return api_key
