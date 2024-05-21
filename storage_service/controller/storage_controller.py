from __future__ import annotations

from storage_service.depends.depend_queue import dependency_queue
from storage_service.depends.depend_s3_service import (
    dependency_storage_service,
)
from storage_service.model.storage.new_file_request import NewFileURLRequest
from storage_service.model.storage.process_file_request import (
    ProcessFileRequest,
)
from storage_service.model.storage.signed_url_response import SignedUrlResponse
from storage_service.service.storage.storage_service import StorageService
from storage_service.utils.file_name_hash import file_name_hash
from storage_service.worker.storage_file_worker import storage_file_worker

from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv
from rq import Queue

s3_router = APIRouter(tags=["storage"])


@cbv(s3_router)
class StorageController:
    queue: Queue = Depends(dependency_queue, use_cache=True)
    storage_service: StorageService = Depends(
        dependency_storage_service, use_cache=True
    )

    @s3_router.post("/file", status_code=200)
    def new_file_url(self, new_file_request: NewFileURLRequest) -> SignedUrlResponse:
        hashed_file_name = file_name_hash(
            new_file_request.file_key, new_file_request.file_postfix
        )

        return self.storage_service.get_temp_upload_link(
            hashed_file_name, new_file_request.file_type
        )

    @s3_router.get("/file", status_code=200)
    def file_url(self, file_key: str, file_postfix: str) -> SignedUrlResponse:
        return self.storage_service.get_temp_read_link(
            file_name_hash(file_key, file_postfix)
        )

    @s3_router.delete("/file", status_code=204)
    def delete_file(self, file_key: str, file_postfix: str):
        return self.storage_service.delete_file(file_name_hash(file_key, file_postfix))

    @s3_router.post("/file/process", status_code=200)
    def process_file(self, process_file_request: ProcessFileRequest):
        self.queue.enqueue(
            storage_file_worker,
            process_file_request.file_key,
            process_file_request.file_postfix,
        )
