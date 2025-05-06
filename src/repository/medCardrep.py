from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel

from src.models.medcard_models import MedCardsOrm
from src.shemas.medCard import MedCard
from src.repository.baseRep import BaseRepository




class MedCardRepository(BaseRepository):
    model = MedCardsOrm
    chema = MedCard