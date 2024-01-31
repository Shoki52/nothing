from typing import Optional

from pydantic import BaseModel


class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    photo: Optional[str] = None
    description: Optional[str] = None
    availability: Optional[bool] = None
    produced_country: Optional[str] = None
    produced_company: Optional[str] = None
    category: Optional[str] = None
