from __future__ import annotations

from storage_service.service.storage_service import StorageService
from storage_service.utils.enums.file_type import FileType
from storage_service.utils.file_handler import FILE_HANDLER

import boto3

import io
from typing import Any


class AmazonS3Service(StorageService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__validate_config(**kwargs)

        self.bucket_name = kwargs.get("bucket_name")
        self.region_name = kwargs.get("region_name")

        self.expires_in = kwargs.get("expires_in")

        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=kwargs.get("aws_access_key_id"),
            aws_secret_access_key=kwargs.get("aws_secret_access_key"),
            region_name=kwargs.get("region_name"),
        )

    def get_temp_upload_link(
        self, file_name, file_type: FileType
    ) -> dict[str, str | Any]:
        return {
            "presigned_url": self._get_presigned_write_url(file_name, file_type),
            "file_key": self._get_object_url(file_name),
        }

    def get_temp_read_link(self, file_name) -> dict[str, str | None]:
        return {"presigned_url": self._get_presigned_read_url(file_name)}

    def process_file(self, file_name: str, file_type: FileType = FileType.PNG) -> None:
        file_bytes = self._get_file_obj(file_name)
        handler = FILE_HANDLER[file_type]["handler"]

        self._upload_file(file_name, handler(file_bytes))

    def _get_object_url(self, file_name: str) -> str:
        return f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{file_name}"

    def _get_presigned_write_url(self, file_name, file_type: FileType) -> str:
        return self.s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": file_name,
                "ContentType": FILE_HANDLER[file_type]["content_type"],
            },
            ExpiresIn=self.expires_in,
        )

    def _get_presigned_read_url(self, file_name) -> str | None:
        result = self.s3.list_objects(Bucket=self.bucket_name, Prefix=file_name)

        if file_name in map(lambda x: x["Key"], result["Contents"]):
            return self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": file_name},
                ExpiresIn=self.expires_in,
            )
        return None

    def _get_file_obj(self, file_name: str) -> io.BytesIO:
        return io.BytesIO(
            self.s3.get_object(Bucket=self.bucket_name, Key=file_name)["Body"].read()
        )

    def _upload_file(self, file_name: str, file_bytes: io.BytesIO) -> None:
        self.s3.upload_fileobj(file_bytes, Bucket=self.bucket_name, Key=file_name)

    @staticmethod
    def __validate_config(**kwargs):
        if not kwargs.get("bucket_name"):
            raise RuntimeError("bucket_name is required")

        if not kwargs.get("aws_access_key_id"):
            raise RuntimeError("aws_access_key_id is required")

        if not kwargs.get("aws_secret_access_key"):
            raise RuntimeError("aws_secret_access_key is required")

        if not kwargs.get("region_name"):
            raise RuntimeError("region_name is required")

        if not kwargs.get("bucket_name"):
            raise RuntimeError("bucket_name is required")
