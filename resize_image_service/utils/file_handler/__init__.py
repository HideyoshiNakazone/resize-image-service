from resize_image_service.utils.enums.file_type import FileType
from resize_image_service.utils.file_handler.handlers.image_handler import (
    image_handler,
)

FILE_HANDLER = {
    FileType.PNG: {"content_type": "image/png", "handler": image_handler},
    FileType.JPEG: {"content_type": "image/jpeg", "handler": image_handler},
}
