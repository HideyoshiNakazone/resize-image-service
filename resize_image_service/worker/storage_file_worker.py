from resize_image_service.depends.depend_s3_service import (
    dependency_storage_service,
)


def storage_file_worker(string_url: str) -> None:
    dependency_storage_service().process_image(string_url)
