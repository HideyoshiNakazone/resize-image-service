from fastapi_utils.cbv import cbv

from fastapi_utils.inferring_router import InferringRouter

health_router = InferringRouter()

@cbv(health_router)
class HealthCheckerController:
    @health_router.get("/health", status_code=200)
    def health(self) -> dict[str, str]:
        return {"status": "healthy"}
