from dataclasses import field
from typing import List

from pydantic.dataclasses import dataclass
from pydantic.main import BaseModel


class Config:
    orm_mode = True


# ------------------------------ InputModel ------------------------------
@dataclass(config=Config)
class FormUser:
    uid: str
    name: str
    email: str
    password: str
    password_re: str
    phone: str


@dataclass(config=Config)
class FormLoginByAdmin:
    id: str
    password: str


@dataclass(config=Config)
class FormLoginByClient:
    id: str
    password: str


# ------------------------------ OutputModel ------------------------------
class UserModel(BaseModel):
    user_id: str = None
    user_name: str = None
    mobile: str = None
    email: str = None
    gender: str = None
    birth: str = None
