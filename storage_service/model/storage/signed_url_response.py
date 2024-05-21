from pydantic import BaseModel


class SignedUrlResponse(BaseModel):
    signed_url: str
    expires_in: int
