from typing import List, Optional

from pydantic import BaseModel


# --- USER --- #

class UserBase(BaseModel):
    # id: int
    name: str
    email: str
    role_id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


# --- ROLE --- #

class RoleBase(BaseModel):
    # id: int
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int
    users: List[User] = []

    class Config:
        orm_mode = True


# --- PHONE --- #

class PhoneBase(BaseModel):
    # id: int
    name: str
    telephone: str
    address: str


class PhoneCreate(PhoneBase):
    pass


class Phone(PhoneBase):
    id: int

    class Config:
        orm_mode = True


# --- SERIAL NUMBER --- #

class SerialNumberBase(BaseModel):
    serial_number: str


class SerialNumberCreate(SerialNumberBase):
    pass


class SerialNumber(SerialNumberBase):
    class Config:
        orm_mode = True
