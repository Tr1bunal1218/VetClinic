from pydantic import BaseModel
from datetime import date
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
class MedRequestAdd(BaseModel):
    name: str
    quantity: int
    min_stock: int

class MedUpdate(BaseModel):
    last_ordered: datetime
    quantity: int
class MedAdd(MedRequestAdd):
    clinic_id: int
    last_ordered: datetime
class Med(MedAdd):
    id:int