from pydantic import BaseModel


class OrderResponseSchema(BaseModel):
    order_id: int
    order_price: int
    delivery_status: str
    delivery_address: str
