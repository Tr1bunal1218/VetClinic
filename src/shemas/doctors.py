from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field
from typing import Optional



class DoctorRequestAdd(BaseModel):
    first_name: str
    last_name: str
    specialization: str
    license_number: str

class DoctorAdd(DoctorRequestAdd):
    clinic_id:int
    
class Doctor(DoctorAdd):
    id: int