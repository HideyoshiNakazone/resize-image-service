from resize_image_service.depends.depend_queue import dependency_queue
from resize_image_service.depends.depend_s3_service import (
    dependency_s3_service,
)
from resize_image_service.service.s3_service import S3Service
from resize_image_service.utils.enums.file_type import FileType
from resize_image_service.utils.file_name_hash import file_name_hash
from resize_image_service.worker.s3_image_worker import s3_image_worker

from fastapi import Body, Depends, Form
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from rq import Queue

from typing import Annotated

s3_router = InferringRouter()


@cbv(s3_router)
class S3Controller:
    queue: Queue = Depends(dependency_queue, use_cache=True)
    s3_service: S3Service = Depends(dependency_s3_service, use_cache=True)

    @s3_router.get("/new_file_url/", status_code=200)
    def new_file_url(
        self,
        username: Annotated[str, Form()],
        file_postfix: Annotated[str, Form()],
        file_type: Annotated[FileType, Form()],
    ) -> dict[str, str]:
        return self.s3_service.get_temp_upload_link(
            file_name_hash(username, file_postfix), file_type
        )

    @s3_router.get("/file_url/", status_code=200)
    def file_url(
        self, username: Annotated[str, Form()], file_postfix: Annotated[str, Form()]
    ) -> dict[str, str]:
        return self.s3_service.get_temp_read_link(
            file_name_hash(username, file_postfix)
        )

    @s3_router.post("/process_image/", status_code=200)
    def process_image(self, string_url: Annotated[str, Body(embed=True)]):
        self.queue.enqueue(s3_image_worker, string_url)
