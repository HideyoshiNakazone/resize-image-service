import logging

from storage_service.depends.depend_s3_service import (
    dependency_storage_service,
)
from storage_service.utils.file.file_hash_generator import generate_file_hash


logger = logging.getLogger(__name__)


def storage_file_worker(username: str, file_postfix: str) -> None:
    storage_service = dependency_storage_service()

    file_name = generate_file_hash(username, file_postfix)
    try:
        stats = storage_service.process_file(file_name)

        print(
            f"File processed: {file_name} - "
            f"Previous Size: {stats["previous_size"]/1_000}kb - "
            f"New Size: {stats["current_size"]/1_000}kb"
        )
    except Exception as e:
        print(
            f"Error processing file: {e}."
            f" Deleting file: {file_name}."
        )

        storage_service.delete_file(file_name)
