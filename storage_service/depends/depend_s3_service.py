from storage_service.config.config_s3 import get_config_s3
from storage_service.service.storage.amazon_s3_service import AmazonS3Service
from storage_service.service.storage.storage_service import StorageService
from storage_service.utils.enums.storage_type import StorageType

import boto3
import botocore.client
from dotenv import load_dotenv

import os
from functools import cache


@cache
def dependency_storage_service() -> StorageService:
    load_dotenv()

    if StorageType(os.environ["STORAGE_TYPE"]) == StorageType.S3_STORAGE:
        s3_config = get_config_s3()

        if "aws_access_key_id" not in s3_config:
            raise RuntimeError("Invalid S3 Config: Missing aws_access_key_id")

        if "aws_secret_access_key" not in s3_config:
            raise RuntimeError("Invalid S3 Config: Missing aws_secret_access_key")

        if "region_name" not in s3_config:
            raise RuntimeError("Invalid S3 Config: Missing region_name")

        s3_client = boto3.client(
            "s3",
            region_name=s3_config["region_name"],
            aws_access_key_id=s3_config["aws_access_key_id"],
            aws_secret_access_key=s3_config["aws_secret_access_key"],
        )

        return AmazonS3Service(
            s3_client,
            s3_config["bucket_name"],
        )

    raise RuntimeError("Invalid Storage Type")
