from storage_service.config.config_s3 import get_config_s3
from storage_service.service.storage.amazon_s3_service import AmazonS3Service
from storage_service.service.storage.storage_service import StorageService
from storage_service.utils.enums.storage_type import StorageType

import boto3
import botocore.client
from dotenv import load_dotenv

import os
from functools import cache


def build_client_s3(config: dict) -> botocore.client.BaseClient:
    if "aws_endpoint_url" not in config:
        config["aws_endpoint_url"] = "https://s3.amazonaws.com"

    if "aws_access_key_id" not in config:
        raise RuntimeError("Invalid S3 Config: Missing aws_access_key_id")

    if "aws_secret_access_key" not in config:
        raise RuntimeError("Invalid S3 Config: Missing aws_secret_access_key")

    if "region_name" not in config:
        raise RuntimeError("Invalid S3 Config: Missing region_name")

    return boto3.client(
        "s3",
        endpoint_url=config["aws_endpoint_url"],
        region_name=config["region_name"],
        aws_access_key_id=config["aws_access_key_id"],
        aws_secret_access_key=config["aws_secret_access_key"],
    )


@cache
def dependency_storage_service() -> StorageService:
    load_dotenv()

    if StorageType(os.environ["STORAGE_TYPE"]) == StorageType.S3_STORAGE:
        s3_config = get_config_s3()

        return AmazonS3Service(
            build_client_s3(s3_config),
            s3_config["bucket_name"],
        )

    raise RuntimeError("Invalid Storage Type")
