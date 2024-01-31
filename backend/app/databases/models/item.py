from sqlalchemy.orm import relationship
from app.databases.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, LargeBinary, Boolean
from app.databases.models.order_item import orders_items


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, nullable=False)
    # ID из таблицы Category
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    # Пока не уверен верный тип данных или нет
    photo = Column(String, nullable=False)
    description = Column(String, nullable=False)
    availability = Column(Boolean, nullable=False)
    produced_country = Column(String, nullable=False)
    produced_company = Column(String, nullable=False)
    # Many to Many
    orders = relationship("Order", secondary=orders_items, back_populates="items")
