from pydantic import BaseModel


class ProcessFileRequest(BaseModel):
    file_key: str
    file_postfix: str
