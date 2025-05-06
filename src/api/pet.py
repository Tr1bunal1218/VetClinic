from fastapi import Query, Body, APIRouter, Path

from src.shemas.pet import *
from src.db import new_session
from src.repository.petRep import PetRepository
from src.api.dependencies import UserDependecies, DBDep
router = APIRouter(prefix="/pets", tags=["Петы"])



@router.post("/{pet_id}")
async def add_pets(user_id: UserDependecies, db: DBDep, data: PetRequestAdd = Body()):
    add_pet_data = PetAdd(user_id=user_id, **data.model_dump())
    res = await db.pets.add_one(add_pet_data)
    await db.commit()
    return res

@router.get("")
async def get_pets(user_id: UserDependecies, db: DBDep):
    return await db.pets.get_filtred(user_id=user_id)

