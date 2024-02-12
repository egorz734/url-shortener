from pydantic import BaseModel


class UrlBase(BaseModel):
    url: str


class UrlCreate(UrlBase):
    pass


class Url(UrlBase):
    id: int
    owner_id: int
    encoded_url: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    urls: list[Url] = []

    class Config:
        orm_mode = True
