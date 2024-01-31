from sqlalchemy.orm import relationship
from app.databases.models.order import Order  # импортирую класс, чтоб не было ошибки, потому что не нашло Order
from app.databases.db import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    hash_of_password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    # One to Many
    orders = relationship("Order")
