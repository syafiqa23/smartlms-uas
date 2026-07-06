from typing import Optional

from ninja import Schema
from pydantic import Field, field_validator


class UserSchema(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    avatar: Optional[str] = None
    bio: str

    @staticmethod
    def resolve_avatar(obj):
        return obj.avatar.url if obj.avatar else None


class UserRegisterSchema(Schema):
    username: str = Field(..., min_length=5, examples=["student01"])
    email: str = Field(..., examples=["student@example.com"])
    password: str = Field(..., min_length=8, examples=["password123"])
    first_name: str = Field("", examples=["Budi"])
    last_name: str = Field("", examples=["Santoso"])
    role: str = Field("student", examples=["student"])

    @field_validator("password")
    @classmethod
    def password_must_contain_number(cls, value):
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number.")
        return value


class LoginSchema(Schema):
    username: str = Field(..., examples=["student01"])
    password: str = Field(..., examples=["UasSmart98765"])


class TokenPairSchema(Schema):
    access: str
    refresh: str
    token_type: str = "Bearer"


class RefreshTokenSchema(Schema):
    refresh: str


class AccessTokenSchema(Schema):
    access: str
    token_type: str = "Bearer"


class UserUpdateSchema(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    role: Optional[str] = None


class ChangePasswordSchema(Schema):
    old_password: str
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def password_must_contain_number(cls, value):
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number.")
        return value
