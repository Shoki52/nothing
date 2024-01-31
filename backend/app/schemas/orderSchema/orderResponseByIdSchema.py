from typing import List
from app.schemas.orderSchema.orderResponseSchema import OrderResponseSchema

from app.schemas.productSchema.productOrderResponseSchema import ProductOrderResponseSchema


class OrderResponseByIdSchema(OrderResponseSchema):
    products_amount: float
    products: List[ProductOrderResponseSchema]
