from pydantic import BaseModel


class ProductCreateSchema(BaseModel):
    name: str
    price: float
    description: str
    availability: bool
    produced_country: str
    produced_company: str
    category: str
