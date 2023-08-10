from __future__ import annotations

from resize_image_service.utils.enums.file_type import FileType

from abc import ABC, abstractmethod
from typing import Any


class StorageService(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def get_temp_upload_link(
        self, file_name, file_type: FileType
    ) -> dict[str, str | Any]:
        pass

    @abstractmethod
    def get_temp_read_link(self, file_name) -> dict[str, str | Any]:
        pass

    @abstractmethod
    def process_file(self, file_name) -> None:
        pass
