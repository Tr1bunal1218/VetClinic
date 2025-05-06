# from fastapi import APIRouter, Path

# from src.shemas.booking import BookingRequestAdd, BookingAdd
# from src.api.dependencies import DBDep
# from src.api.dependencies import UserDependecies

# router = APIRouter(prefix="/bookings", tags=["Запись приема Пета"])

# @router.post("/{booking_id}",)
# async def create_booking(
#     db: DBDep,
#     user_id: UserDependecies,
#     bookingRequestAdd: BookingRequestAdd,
#     booking_id: int = Path()
#     ):
    
#     user_data = await db.users.get_one_or_none(id=user_id)
    
#     pet_data = await db.pets.get_one_or_none(id=bookingRequestAdd.pet_id)
    
#     res = BookingAdd(user_id=user_data.id, **bookingRequestAdd.model_dump())
#     print(res)
#     res_data = await db.bookings.add_one(res)
#     print("РЕЕЕС ДАТА-",res_data)
#     await db.commit()
    
#     return {"status": "ok", "data": res_data}

# @router.get("", name="Получить все записи",)
# async def get_bookings(db: DBDep):
#     return await db.bookings.get_all()

# @router.get("/me", name="Получить записи у текущего пользователя")
# async def get_my_bookings(db: DBDep, user_id: UserDependecies):
#     return await db.bookings.get_filtred(user_id=user_id) 