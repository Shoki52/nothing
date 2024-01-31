from pydantic import BaseModel


class ProductAddOrderSchema(BaseModel):
    id: int = 1
    amount: float = 1
