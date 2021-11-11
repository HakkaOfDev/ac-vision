from pydantic import BaseModel


class UsersBase(BaseModel):
    email: str
    login: str


class Users(UsersBase):
    id: int
    first_name: str
    last_name: str
    role: str


class UserCreate(Users):
    password: str

    class Config:
        orm_mode = True
