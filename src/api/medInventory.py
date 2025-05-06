from fastapi import APIRouter, Path
import datetime
from src.api.dependencies import DBDep
from src.service.InventoryService import InventoryService
from src.shemas.MedicationInventory import *
router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("/check/{clinic_id}")
async def check_medications(db: DBDep, clinic_id: int = Path()):
    inv = InventoryService(db)
    if not await inv.check_and_order_medications(clinic_id):
        return {"Status":"Ok"}

@router.post("/{clinic_id}")
async def add_inventory(db: DBDep, data: MedRequestAdd, clinic_id: int = Path()):
    add_data = MedAdd(last_ordered=datetime.now(), clinic_id=clinic_id, **data.model_dump())
    res = await db.medInvent.add_one(add_data)
    await db.commit()
    return res
    