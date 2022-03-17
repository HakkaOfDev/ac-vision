from pydantic import BaseModel, stricturl
from typing import Optional



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
    

class Setting(BaseModel):
    name: str
    value: str


class Notification(BaseModel):
    onuid: int
    gponPort: int
    reason: Optional[str]
    status: str
    date: str