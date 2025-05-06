
from src.models.clinics import ClinicOrm
from src.repository.baseRep import BaseRepository
from src.shemas.clinics import Clinic

class ClinicsRepository(BaseRepository):
    model = ClinicOrm
    chema = Clinic