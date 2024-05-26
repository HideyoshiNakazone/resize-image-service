from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "details": {
                    "body": exc.body,
                    "errors": exc.errors(),
                },
                "status_code": status_code,
            }
        },
    )
