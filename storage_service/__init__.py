from storage_service.config.config_allowed_origins import get_allowed_origins
from storage_service.controller import health_router, storage_router
from storage_service.utils.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
)

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(storage_router)
app.include_router(health_router)
