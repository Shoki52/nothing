from typing import List

from pydantic import BaseModel

from app.schemas.productSchema.productResponseSchema import ProductResponseSchema


class ProductAllResponseSchema(BaseModel):
    products: List[ProductResponseSchema]
    products_amount: float
