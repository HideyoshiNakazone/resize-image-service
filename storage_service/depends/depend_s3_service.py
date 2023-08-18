from storage_service.config.config_s3 import get_config_s3
from storage_service.service.amazon_s3_service import AmazonS3Service
from storage_service.service.storage_service import StorageService
from storage_service.utils.enums.storage_type import StorageType

from dotenv import load_dotenv

import os
from functools import cache


@cache
def dependency_storage_service() -> StorageService:
    load_dotenv()

    if StorageType(os.environ["STORAGE_TYPE"]) == StorageType.S3_STORAGE:
        return AmazonS3Service(**get_config_s3())

    raise RuntimeError("Invalid Storage Type")
