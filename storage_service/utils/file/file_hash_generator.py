import base64
from hashlib import md5


def generate_file_hash(file_key: str, file_postfix: str) -> str:
    hashed_file_key = md5(file_key.encode("utf-8")).digest()
    hashed_file_key = base64.b64encode(hashed_file_key).decode()

    return f"{hashed_file_key}_{file_postfix}"
