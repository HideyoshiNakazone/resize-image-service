from resize_image_service.depends.depend_s3_service import (
    dependency_s3_service,
)


def s3_image_worker(string_url: str) -> None:
    dependency_s3_service().process_image(string_url)
