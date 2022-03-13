from pydantic import BaseModel
from typing import Optional

from api.src.components.sql_app.database import Base


class UsersBase(BaseModel):
    email: str
    login: Optional[str]


class Users(UsersBase):
    id: Optional[int]
    first_name: str
    last_name: str
    role: str


class UserCreate(Users):
    password: str

    class Config:
        orm_mode = True

class Onusd(BaseModel):
    onuid: int
    description: str
    

class olt_setting(BaseModel):
    ip: str

