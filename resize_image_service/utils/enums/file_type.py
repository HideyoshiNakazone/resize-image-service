from enum import Enum


class FileType(Enum):
    PNG = "png"
    JPEG = "jpeg"


CONTENT_TYPE = {FileType.PNG: "image/png", FileType.JPEG: "image/jpeg"}
