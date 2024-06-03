from pydantic import BaseModel, EmailStr
from enum import Enum

class Roles(Enum):
    user = "user"
    admin = "admin"

class UserSchema(BaseModel):
    email: EmailStr
    name: str
    surname: str
    password: str

    class Config:
        orm_mode = True
