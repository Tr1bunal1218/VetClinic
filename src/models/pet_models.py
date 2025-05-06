from sqlalchemy import ForeignKey, String
from src.db import BaseOrm
from sqlalchemy.orm import Mapped, mapped_column


class PetsOrm(BaseOrm):
    __tablename__ = "Pets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    breed: Mapped[str | None]
    name: Mapped[str]
    age: Mapped[int | None]
    sex: Mapped[str | None]
    vid: Mapped[str | None]