from fastapi import Query, Body, APIRouter, Path
from src.shemas.medCard import MedCardRequestAdd, MedCardAdd
from src.db import new_session

from sqlalchemy import insert, select, delete, update

from src.repository.medCardrep import MedCardRepository
router = APIRouter(prefix="/pets", tags=["Медецинские карты Петов"])

@router.get("/{pet_id}/cards", name="Получить все медецинские карты")
async def get_cards(pet_id: int):
    async with new_session() as session:
        return await MedCardRepository(session).get_filtred(pet_id=pet_id)

@router.get("/{pet_id}/cards/{medCard_id}", name="Получить мед.карту у Пета")
async def get_card_by_id(pet_id: int, medCard_id: int):
    async with new_session() as session:
        return await MedCardRepository(session).get_one_or_none(id=medCard_id, pet_id=pet_id)

@router.post("/{pet_id}/cards", name="добавить в БД медецинскую карту")
async def add_rooms(pet_id: int, data: MedCardRequestAdd = Body()):
    async with new_session() as session:
        res = MedCardAdd(pet_id=pet_id, **data.model_dump())
        result = await MedCardRepository(session).add_one(res)
        await session.commit()
        return result