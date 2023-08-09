from resize_image_service.config.config_s3 import get_config_s3
from resize_image_service.service.s3_service import S3Service

from functools import cache


@cache
def dependency_s3_service() -> S3Service:
    return S3Service(**get_config_s3())
