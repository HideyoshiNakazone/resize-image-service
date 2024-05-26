from storage_service.model.health_check.health_check_response import (
    HealthCheckResponse,
)

from fastapi import APIRouter
from fastapi_utils.cbv import cbv

router = APIRouter(tags=["health"])


@cbv(router)
class HealthCheckerController:
    @router.get("/health", status_code=200)
    def health(self) -> HealthCheckResponse:
        return HealthCheckResponse(status="healthy")
