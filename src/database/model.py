from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# declare all needed database models here


# dummy model, delete it while setting up the project
class DummyModel(Base):
    __tablename__ = "dummy"
    id = Column(Integer, primary_key=True)
    name = Column(String)

class DatabaseUser(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True)
    name = Column(String, nullable=False)
