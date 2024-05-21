from __future__ import annotations

import logging

from storage_service.depends.depend_virus_checker_service import (
    dependency_virus_checker_service,
)
from storage_service.model.storage.signed_url_response import SignedUrlResponse
from storage_service.service.storage.storage_service import StorageService
from storage_service.service.virus_checker.virus_checker_service import (
    VirusCheckerService,
)
from storage_service.utils.enums.file_type import FileType

from botocore.client import BaseClient

import io


logger = logging.getLogger(__name__)


class AmazonS3Service(StorageService):
    virus_checker_service: VirusCheckerService

    s3_client: BaseClient
    bucket_name: str

    expires_in: int = 3600

    def __init__(
        self,
        s3_client: BaseClient,
        bucket_name: str,
        virus_checker_service=None,
        **kwargs,
    ):
        self.virus_checker_service = virus_checker_service

        if s3_client is None:
            raise RuntimeError("Invalid S3 Config: Missing s3_client")
        self.s3_client = s3_client

        if bucket_name is None:
            raise RuntimeError("Invalid S3 Config: Missing bucket_name")
        self.bucket_name = bucket_name

        if virus_checker_service is None:
            self.virus_checker_service = dependency_virus_checker_service()

        if "expires_in" in kwargs:
            self.expires_in = kwargs["expires_in"]

    def get_temp_upload_link(self, file_name, file_type: FileType) -> SignedUrlResponse:
        return SignedUrlResponse(
            signed_url=self._get_presigned_write_url(file_name, file_type),
            expires_in=self.expires_in,
        )

    def get_temp_read_link(self, file_name) -> SignedUrlResponse:
        return SignedUrlResponse(
            signed_url=self._get_presigned_read_url(file_name),
            expires_in=self.expires_in,
        )

    def delete_file(self, file_name: str) -> None:
        self._delete_file(file_name)

    def process_file(self, file_name: str, file_type: FileType = FileType.PNG) -> dict:
        try:
            file_bytes = self._get_file_obj(file_name)
        except Exception as _:
            raise FileNotFoundError("File not found")

        if not self.virus_checker_service.check_virus(file_bytes):
            raise ValueError("Virus Detected")

        try:
            old_size = file_bytes.getbuffer().nbytes

            file_bytes = file_type.get_validator()(file_bytes)

            new_size = file_bytes.getbuffer().nbytes
        except Exception as _:
            raise RuntimeError("Error Processing")

        self._upload_file(file_name, file_bytes)

        return {
            "previous_size": old_size,
            "current_size": new_size,
        }

    def _get_presigned_write_url(self, file_name, file_type: FileType) -> str:
        return self.s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": file_name,
                "ContentType": file_type.get_content_type(),
            },
            ExpiresIn=self.expires_in,
        )

    def _get_presigned_read_url(self, file_name) -> str | None:
        result = self.s3_client.list_objects(Bucket=self.bucket_name, Prefix=file_name)

        if "Contents" in result and file_name in map(
            lambda x: x["Key"], result["Contents"]
        ):
            return self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket_name, "Key": file_name},
                ExpiresIn=self.expires_in,
            )

        raise FileNotFoundError("File not found")

    def _get_file_obj(self, file_name: str) -> io.BytesIO:
        return io.BytesIO(
            self.s3_client.get_object(Bucket=self.bucket_name, Key=file_name)[
                "Body"
            ].read()
        )

    def _upload_file(self, file_name: str, file_bytes: io.BytesIO) -> None:
        self.s3_client.upload_fileobj(
            file_bytes, Bucket=self.bucket_name, Key=file_name
        )

    def _delete_file(self, file_name: str) -> None:
        self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_name)
