import base64
from hashlib import md5


def file_name_hash(username: str, file_postfix: str) -> str:
    hashed_username = md5(username.encode("utf-8")).digest()
    hashed_username = base64.b64encode(hashed_username).decode()

    return f"{hashed_username}_{file_postfix}"
