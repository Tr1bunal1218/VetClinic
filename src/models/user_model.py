from enum import Enum
from sqlalchemy import String, Enum as SqlEnum
from src.db import BaseOrm
from sqlalchemy.orm import Mapped, mapped_column

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    DEBUG = "debug"

class UsersOrm(BaseOrm):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[UserRole] = mapped_column(SqlEnum(UserRole), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
