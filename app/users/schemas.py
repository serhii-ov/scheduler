"""Schemas are API contract, not DB contract.
    Pydantic models used for request and response payloads.
- Show CRUD implementation using these schemas
- Add validation (email OR phone required) at schema level
- Show how to hash password cleanly
- Align schemas with JWT auth (FastAPI security)
"""
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from enum import Enum

from app.core.phone_normalizer import normalize_phone


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None


class UserRole(str, Enum):
    ADMIN = "admin"
    ELECTRICIAN = "electrician"
    ENGINEER = "engineer"


class BaseUser(BaseModel):
    name: str
    phone_number: str
    email: Optional[EmailStr] = None
    role: UserRole
    is_active: bool = True


class UserCreate(BaseModel):
    phone_number: str
    password: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        # validation only (no DB logic)
        normalize_phone(v)
        return v


class UserCreate(BaseUser):
    password: str

    @field_validator("phone_number")
    def validate_and_normalize_phone(cls, v: str) -> str:
        return normalize_phone(v)   
    


class UserRead(BaseUser):
    id: int

    class Config:
        """
        This allows:
        UserRead.model_validate(sqlalchemy_user)
        """
        from_attributes = True


class UserUpdate(BaseModel):                # Optional: Update schema
    name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
