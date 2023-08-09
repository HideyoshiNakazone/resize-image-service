from resize_image_service.controller.s3_controller import s3_router

from fastapi import FastAPI

app = FastAPI()

app.include_router(s3_router, tags=["s3"], prefix="/s3")
