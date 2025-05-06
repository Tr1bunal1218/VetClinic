from sqlalchemy import String, ForeignKey
from src.db import BaseOrm
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
class MedicationInventoryOrm(BaseOrm):
    __tablename__ = "medications"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    quantity: Mapped[int]
    min_stock: Mapped[int]
    last_ordered: Mapped[datetime]
    clinic_id: Mapped[int] = mapped_column(ForeignKey("clinics.id"))