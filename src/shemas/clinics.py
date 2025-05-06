from pydantic import BaseModel, Field, EmailStr
from datetime import date

class ClinicAdd(BaseModel):
    name: str
    address: str
    phone: str
    email: EmailStr
    license_number: str
    established_date: date
    
class Clinic(ClinicAdd):
    id: int