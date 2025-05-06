from fastapi import APIRouter, Path
import datetime
from src.api.dependencies import DBDep
from src.shemas.clinics import *


router = APIRouter(prefix="/clinic", tags=["Клиники"])

@router.get("")
async def get_all_clinics(db: DBDep):
    return await db.clinics.get_all()

@router.post("/{clinic_id}")
async def add_clinic(data: ClinicAdd, db: DBDep):
    res = await db.clinics.add_one(data)
    await db.commit()
    return res
    