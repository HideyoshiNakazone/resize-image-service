from storage_service.utils.enums.file_type import FileType

from pydantic import BaseModel


class NewFileURLRequest(BaseModel):
    file_key: str
    file_postfix: str
    file_type: FileType
