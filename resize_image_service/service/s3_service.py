from resize_image_service.utils.enums.file_type import CONTENT_TYPE, FileType

import boto3
from PIL import Image

import io
from typing import Any, Dict


class S3Service:
    def __init__(self, **kwargs):
        self.__validate_config(**kwargs)

        self.bucket_name = kwargs.get("bucket_name")
        self.region_name = kwargs.get("region_name")
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
            "presigned_url": self._get_presigned_right_url(file_name, file_type),
            "file_key": self._get_object_url(file_name),
        }

    def get_temp_read_link(self, file_name) -> dict[str, str | Any]:
        return {"presigned_url": self._get_presigned_read_url(file_name)}

    def process_image(self, file_name) -> None:
        img = self._get_image_obj(file_name)

        img = self._resize_img(img)
        img = self._remove_img_metadata(img)

        self._upload_image(file_name, img)

    def _get_object_url(self, file_name: str):
        return f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{file_name}"

    def _get_presigned_right_url(self, file_name, file_type: FileType):
        return self.s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": file_name,
                "ContentType": CONTENT_TYPE[file_type],
            },
            ExpiresIn=3600,
        )

    def _get_presigned_read_url(self, file_name):
        return self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": file_name},
            ExpiresIn=3600,
        )

    def _get_image_obj(self, file_name: str):
        object_byte = io.BytesIO(
            self.s3.get_object(Bucket=self.bucket_name, Key=file_name)["Body"].read()
        )

        return Image.open(object_byte)

    def _upload_image(self, file_name: str, img: Image):
        new_byte_img = io.BytesIO()
        img.save(new_byte_img, format="PNG")

        new_byte_img.seek(0)
        self.s3.upload_fileobj(new_byte_img, Bucket=self.bucket_name, Key=file_name)

    @staticmethod
    def _resize_img(img):
        img.thumbnail((320, 320))

        return img

    @staticmethod
    def _remove_img_metadata(img):
        data = list(img.getdata())
        image_without_exif = Image.new(img.mode, img.size)
        image_without_exif.putdata(data)

        return image_without_exif

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
