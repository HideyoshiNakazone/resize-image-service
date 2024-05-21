from fastapi import HTTPException, status


class FileNotFoundException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status.HTTP_400_BAD_REQUEST, detail=message
        )
