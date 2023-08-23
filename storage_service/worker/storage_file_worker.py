from storage_service.depends.depend_s3_service import (
    dependency_storage_service,
)
from storage_service.utils.enums.file_type import FileType
from storage_service.utils.file_name_hash import file_name_hash


def storage_file_worker(username: str, file_postfix: str) -> None:
    dependency_storage_service().process_file(file_name_hash(username, file_postfix))
