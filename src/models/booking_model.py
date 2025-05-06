from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

from src.db import BaseOrm


class BookingOrm(BaseOrm):
    __tablename__ = 'bookings'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    pet_id: Mapped[int] = mapped_column(ForeignKey('Pets.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    doctor_id: Mapped[int] = mapped_column(nullable=True)
    date: Mapped[datetime]
    tg_username: Mapped[str | None]
