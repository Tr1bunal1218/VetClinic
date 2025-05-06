
from src.models.doctors import DoctorOrm
from src.repository.baseRep import BaseRepository
from src.shemas.doctors import Doctor

class DoctorsRepository(BaseRepository):
    model = DoctorOrm
    chema = Doctor