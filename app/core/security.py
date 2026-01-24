from passlib.context import CryptContext       
from datetime import datetime, timedelta
from jose import jwt                            
from typing import Optional

from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
        subject: str,
        expires_delta: Optional[timedelta] = None,
        extra_claims: dict | None = None,
    ) -> str:
    expire = datetime.now() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(
        payload, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM,
        )


def decode_token(token: str) -> str:
    payload = jwt.decode(
        token, 
        settings.SECRET_KEY, 
        algorithms=[settings.ALGORITHM],
        )
    return payload.get("sub")


def is_password_strong(password: str) -> bool:
    """
    Check criteria for a strong password
    """
    min_length = 8
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    return (
        len(password) >= min_length and has_upper and has_lower
            and has_digit and has_special
            )
