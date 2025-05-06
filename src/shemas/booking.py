from pydantic import BaseModel
from datetime import datetime

class BookingRequestAdd(BaseModel):
    pet_id: int
    date: datetime | None = None
    tg_username: str | None = None
class BookingAdd(BookingRequestAdd):
    user_id: int
    doctor_id: int
class Booking(BookingAdd):
    id:int
    
class BookingUpdateTime(BaseModel):
    date: datetime