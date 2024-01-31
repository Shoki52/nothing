from pydantic import BaseModel


class OrderAmountSchema(BaseModel):
    amount: int = 1
