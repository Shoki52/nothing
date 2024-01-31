from pydantic import BaseModel


class AdminLoginSchema(BaseModel):
    login: str = "admin"
    password: str = "admin"
