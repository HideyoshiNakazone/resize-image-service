from fastapi import APIRouter
from fastapi_utils.cbv import cbv

health_router = APIRouter()


@cbv(health_router)
class HealthCheckerController:
    @health_router.get("/health", status_code=200)
    def health(self) -> dict[str, str]:
        return {"status": "healthy"}
