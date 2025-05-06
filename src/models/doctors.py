from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String
from datetime import date
from sqlalchemy.ext.hybrid import hybrid_property

from src.db import BaseOrm

class DoctorOrm(BaseOrm):
    __tablename__ = "doctors"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), index=True)
    last_name: Mapped[str] = mapped_column(String(50), index=True)
    specialization: Mapped[str] = mapped_column(String(100))
    license_number: Mapped[str] = mapped_column(String(50), unique=True)
    clinic_id: Mapped[int] = mapped_column(ForeignKey("clinics.id"))