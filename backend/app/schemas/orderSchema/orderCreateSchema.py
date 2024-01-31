from pydantic import BaseModel
from typing import List
from app.schemas.productSchema.productAddOrderSchema import ProductAddOrderSchema


class OrderCreateSchema(BaseModel):
    products: List[ProductAddOrderSchema]
    delivery_address: str = "город Астана, улица Панфилова, дом 3"
    delivery_status: str = "В ожидании"

