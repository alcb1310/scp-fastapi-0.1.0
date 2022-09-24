from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_uuid: str
    company_uuid: str


class CompanyBase(BaseModel):
    ruc: str
    name: str
    employees: int


class CompanyResponse(CompanyBase):
    uuid: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class CompanyCreate(UserCreate, CompanyBase):
    username: str