from sqlalchemy import Column, Integer, VARCHAR, TEXT

from .database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(VARCHAR(255))
    last_name = Column(VARCHAR(255))
    login = Column(VARCHAR(255), unique=True)
    email = Column(VARCHAR(255), unique=True)
    password = Column(TEXT)
    role = Column(VARCHAR(255))


class Onus(Base):
        __tablename__ = "onus"
        onuid = Column(Integer, primary_key=True, unique=True)
        description = Column(VARCHAR(255))
        
class Olt(Base):
    __tablename__ = "olt"
    ip = Column(VARCHAR(255),primary_key=True, unique=True)

