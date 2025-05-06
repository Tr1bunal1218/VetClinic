from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel

from src.models.pet_models import PetsOrm
from src.shemas.pet import Pet
from src.repository.baseRep import BaseRepository




class PetRepository(BaseRepository):
    model = PetsOrm
    chema = Pet
    async def get_all(self, title, location, limit, offset):
        query = select(PetsOrm)

        if title:
            query = query.where(PetsOrm.title.ilike(f"%{title}%"))
        if location:
            query = query.where(PetsOrm.location.ilike(f"%{location}%"))


        query = query.limit(limit).offset(offset)


        result = await self.session.execute(query)
        return [Pet.model_validate(hotels, from_attributes=True) for hotels in result.scalars().all()]




