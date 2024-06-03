from pydantic import BaseModel, EmailStr


class UserSignupRequest(BaseModel):
    email: EmailStr
    name: str
    surname: str
    password: str


class UserSigninRequest(BaseModel):
    email: EmailStr
    password: str


class FlatCreateRequest(BaseModel):
    name: str
    location: str
    description: str
    area: int
    price: int
    rooms: int

    class Config:
        orm_mode = True
