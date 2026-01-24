from sqlalchemy import (
    String, Boolean, CheckConstraint, Enum,
    )
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.users.roles import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False,
        )  
    email: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=True,
        )
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    role: Mapped[UserRole] = mapped_column(
        Enum(
            "admin",
            "electrician",
            "engineer",
            name="user_roles",
            native_enum=True,
            create_constraint=False,   # avoids CHECK constraints that conflict with enums
        ),
        nullable=False,
        default=UserRole.ELECTRICIAN,
    )

    __table_args__ = (
        CheckConstraint(
            "email IS NOT NULL OR phone_number IS NOT NULL",
            name="ck_user_email_or_phone_required",
        ),
    )
