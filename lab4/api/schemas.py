from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = 'secret'
    authjwt_access_token_expires: int = 86400
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {'access'}


# --- USER --- #

class UserLogin(BaseModel):
    email: str
    password: str


class UserAuthorize(BaseModel):
    salt: str
    hashed_password: str


class UserBase(BaseModel):
    name: str
    email: str
    role_id: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserWithToken(BaseModel):
    user: User
    access_token: str


# --- ROLE --- #

class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True


# --- PHONE --- #

class PhoneBase(BaseModel):
    name: str
    telephone: str
    address: str


class PhoneCreate(PhoneBase):
    pass


class Phone(PhoneBase):
    id: int

    class Config:
        orm_mode = True
