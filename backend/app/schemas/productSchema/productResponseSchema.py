from pydantic import BaseModel


class ProductResponseSchema(BaseModel):
    id: int
    name: str
    price: float
    photo: str
    description: str
    availability: bool
    produced_country: str
    produced_company: str
    category: str

