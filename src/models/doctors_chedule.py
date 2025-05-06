from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from datetime import date
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from src.db import BaseOrm

class DoctorScheduleOrm(BaseOrm):
    __tablename__ = "doctor_schedules"
    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    start_time: Mapped[datetime] = mapped_column()
    end_time: Mapped[datetime] = mapped_column()
    clinic_id: Mapped[int] = mapped_column(ForeignKey("clinics.id"))
