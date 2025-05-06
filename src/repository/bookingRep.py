from pydantic import BaseModel
from sqlalchemy import insert, select
from datetime import datetime

from src.repository.baseRep import BaseRepository
from src.models.booking_model import BookingOrm
from src.shemas.booking import Booking


class BookingRepository(BaseRepository):
    model = BookingOrm
    chema = Booking
    
    async def get_filtred(
    self,
    *,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    **kwargs
):
        query = select(self.model)
        
        # Базовые фильтры
        if kwargs:
            query = query.filter_by(**kwargs)
        
        # Фильтры по дате
        if date_from:
            query = query.where(self.model.date >= date_from)
        if date_to:
            query = query.where(self.model.date <= date_to)
        
        result = await self.session.execute(query)
        return result.scalars().all()
