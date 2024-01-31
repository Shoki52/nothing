from sqlalchemy import Table, Column, ForeignKey, Float
from app.databases.db import Base


orders_items = Table(
    "orders_items",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id")),
    Column("item_id", ForeignKey("items.id")),
    Column('amount', Float)
)
