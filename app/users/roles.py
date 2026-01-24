from sqlalchemy import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    ENGINEER = "engineer"
    ELECTRICIAN = "electrician"
