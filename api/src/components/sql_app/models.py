from email.policy import default
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
        
        
class Setting(Base):
    __tablename__ = "setting"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(255))
    value = Column(VARCHAR(255))


class Notification(Base):
    __tablename__ = "notification"
    id  = Column(Integer, primary_key=True, index=True)
    onuid   = Column(Integer)
    gponPort    = Column(Integer)
    reason  = Column(VARCHAR(255), nullable= True)
    status  = Column(VARCHAR(255))
    date    = Column(VARCHAR(255))
