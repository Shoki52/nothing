from sqlalchemy.orm import relationship
from app.databases.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.databases.models.order_item import orders_items
from app.databases.models.item import Item # импортирую класс, чтоб не было ошибки, потому что не нашло Item


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, nullable=False)
    # ID из таблицы User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    address = Column(String, nullable=False)
    status = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    # Many to Many
    # back_populates - чтоб меняла записи в обоих таблицах
    items = relationship("Item", secondary=orders_items, back_populates="orders")
