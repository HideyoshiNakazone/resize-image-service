from storage_service.model.health_check.health_check_response import (
    HealthCheckResponse,
)

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

health_router = APIRouter(tags=["health"])


@cbv(health_router)
class HealthCheckerController:
    @health_router.get("/health", status_code=200)
    def health(self) -> HealthCheckResponse:
        return HealthCheckResponse(status="healthy")
