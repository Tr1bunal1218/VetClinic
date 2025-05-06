from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel

from src.models.medicationInventory_model import MedicationInventoryOrm
from src.shemas.MedicationInventory import Med
from src.repository.baseRep import BaseRepository




class MedicationInventoryRepository(BaseRepository):
    model = MedicationInventoryOrm
    chema = Med
