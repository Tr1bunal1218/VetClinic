from sqlalchemy import String, ForeignKey
from src.db import BaseOrm
from sqlalchemy.orm import Mapped, mapped_column


class MedCardsOrm(BaseOrm):
    __tablename__ = "MedCards"

    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey("Pets.id"))     
    vactination: Mapped[str | None]
    alergic: Mapped[str | None]
    chronic_diseases: Mapped[str | None]