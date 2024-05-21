from __future__ import annotations

from storage_service.model.storage.signed_url_response import SignedUrlResponse
from storage_service.utils.enums.file_type import FileType

from abc import ABC, abstractmethod


class StorageService(ABC):
    @abstractmethod
    def get_temp_upload_link(self, file_name, file_type: FileType) -> SignedUrlResponse:
        pass

    @abstractmethod
    def get_temp_read_link(self, file_name) -> SignedUrlResponse:
        pass

    @abstractmethod
    def delete_file(self, file_name: str) -> None:
        pass

    @abstractmethod
    def process_file(self, file_name: str, file_type: FileType) -> None:
        pass
