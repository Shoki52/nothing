from pydantic import BaseModel
from app.schemas.productSchema.productAddOrderSchema import ProductAddOrderSchema


class ProductOrderResponseSchema(ProductAddOrderSchema):
    name: str
    photo: str
    price: float
    description: str
    availability: bool
    produced_country: str
    produced_company: str
    category: str
