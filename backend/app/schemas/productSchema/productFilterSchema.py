from typing import Optional

from pydantic import BaseModel


class ProductFilterSchema(BaseModel):
    price: float = None
    sort: int = 0
    availability: Optional[bool] = None
    text: str = ""
    category: str = ""
