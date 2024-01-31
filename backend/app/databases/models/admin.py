from app.databases.db import Base
from sqlalchemy import Column, Integer, String


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, nullable=False)
    hash_of_password = Column(String, nullable=False)
    name = Column(String, nullable=False, unique=True)
