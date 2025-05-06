from src.models.doctors_chedule import DoctorScheduleOrm
from src.repository.baseRep import BaseRepository
from src.shemas.doctors_schedule import Schedule
from datetime import datetime, timezone
from sqlalchemy import select

class DoctorsScheduleRepository(BaseRepository):
    model = DoctorScheduleOrm
    chema = Schedule
    
    async def get_current_schedule(
        self, 
        doctor_id: int, 
        booking_time: datetime
    ):
        
        naive = booking_time.replace(tzinfo=None)
        res = await self.session.execute(
            select(DoctorScheduleOrm)
            .filter(
                DoctorScheduleOrm.doctor_id == doctor_id,
                DoctorScheduleOrm.start_time <= naive,
                DoctorScheduleOrm.end_time >= naive
            )
        )
        
        return res if res else None