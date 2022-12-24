from typing import Optional

from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: str
    encrypted_password: str
    email: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False

    class Config:
        orm_mode = True


class LoginUserInfo(BaseModel):
    user_id: str
    password: str


class RegisterUserInfo(BaseModel):
    user_id: str
    password: str
    email: Optional[str] = None