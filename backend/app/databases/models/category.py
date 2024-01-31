from sqlalchemy.orm import relationship
from app.databases.models.item import Item # импортирую класс, чтоб не было ошибки, потому что не нашло Item
from app.databases.db import Base
from sqlalchemy import Column, Integer, String


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, unique=True, nullable=False)
    photo = Column(String, unique=True, nullable=False)
    # One to Many
    items = relationship("Item")
