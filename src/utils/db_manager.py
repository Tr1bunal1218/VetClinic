from src.repository.petRep import PetRepository
from src.repository.medCardrep import MedCardRepository
from src.repository.userRep import UserRepository
from src.repository.bookingRep import BookingRepository
from src.repository.clinicsRep import ClinicsRepository
from src.repository.doctorsRep import DoctorsRepository
from src.repository.medInventoryRep import MedicationInventoryRepository
from src.repository.doctorsScheduleRep import DoctorsScheduleRepository

class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory
    
    async def __aenter__(self):
        self.session = self.session_factory()
        
        self.pets = PetRepository(self.session)
        self.card = MedCardRepository(self.session)
        self.users = UserRepository(self.session)
        self.bookings = BookingRepository(self.session)
        self.clinics = ClinicsRepository(self.session)
        self.doctors = DoctorsRepository(self.session)
        self.medInvent = MedicationInventoryRepository(self.session)
        self.doctorsSchedule = DoctorsScheduleRepository(self.session)
        return self
        
    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()
        
    async def commit(self):
        await self.session.commit()