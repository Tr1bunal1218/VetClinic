from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field
from typing import Optional

class ScheduleRequestAdd(BaseModel):
    start_time: datetime
    end_time: datetime
class ScheduleAdd(ScheduleRequestAdd):
    clinic_id: int
    doctor_id: int
class Schedule(ScheduleAdd):
    id: int
    
class ScheduleRequestUpdate(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None
    
class ScheduleUpdate(ScheduleRequestUpdate):
    clinic_id: int | None = None
    