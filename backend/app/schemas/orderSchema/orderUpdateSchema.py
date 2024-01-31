from pydantic import BaseModel


class OrderUpdateSchema(BaseModel):
    delivery_status: str = "В ожидании"
