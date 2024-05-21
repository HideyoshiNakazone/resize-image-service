from enum import Enum
from io import BytesIO
from typing import Callable

from storage_service.utils.file.validators import image_validator


class FileType(Enum):
    PNG = "png"
    JPEG = "jpeg"

    def get_content_type(self) -> str:
        match self:
            case FileType.PNG:
                return "image/png"
            case FileType.JPEG:
                return "image/jpeg"
            case _:
                raise ValueError("File Type Not Implemented")

    def get_validator(self) -> Callable[[BytesIO], BytesIO]:
        match self:
            case FileType.PNG | FileType.JPEG:
                return image_validator
            case _:
                raise ValueError("File Type Not Implemented")
