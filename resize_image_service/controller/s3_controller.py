from resize_image_service.depends.depend_queue import dependency_queue
from resize_image_service.depends.depend_s3_service import (
    dependency_storage_service,
)
from resize_image_service.service.storage_service import StorageService
from resize_image_service.utils.enums.file_type import FileType
from resize_image_service.utils.file_name_hash import file_name_hash
from resize_image_service.worker.storage_file_worker import storage_file_worker

from fastapi import Body, Depends, Form
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from rq import Queue

from typing import Annotated

s3_router = InferringRouter()


@cbv(s3_router)
class S3Controller:
    queue: Queue = Depends(dependency_queue, use_cache=True)
    storage_service: StorageService = Depends(dependency_storage_service, use_cache=True)

    @s3_router.get("/new_file_url/", status_code=200)
    def new_file_url(
        self,
        username: Annotated[str, Body(embed=True)],
        file_postfix: Annotated[str, Body(embed=True)],
        file_type: Annotated[FileType, Body(embed=True)],
    ) -> dict[str, str]:
        return self.storage_service.get_temp_upload_link(
            file_name_hash(username, file_postfix), file_type
        )

    @s3_router.get("/file_url/", status_code=200)
    def file_url(
        self,
        username: Annotated[str, Body(embed=True)],
        file_postfix: Annotated[str, Body(embed=True)],
    ) -> dict[str, str]:
        return self.storage_service.get_temp_read_link(
            file_name_hash(username, file_postfix)
        )

    @s3_router.post("/process_file/", status_code=200)
    def process_file(self, string_url: Annotated[str, Body(embed=True)]):
        self.queue.enqueue(storage_file_worker, string_url)
