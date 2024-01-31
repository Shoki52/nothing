from pydantic import BaseModel


class UserResponseSchema(BaseModel):
    success: bool
    access_token: str

