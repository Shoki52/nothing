from pydantic import BaseModel


class UserRegisterSchema(BaseModel):
    phone_int: str = "88005553535"
    password: str = "12345678"
