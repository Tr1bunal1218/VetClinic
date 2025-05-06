from fastapi import APIRouter, Path, Body

from src.shemas.doctors import *
from src.api.dependencies import DBDep
from src.service.BookingService import BookingService
from src.shemas.booking import *
from src.api.dependencies import UserDependecies
from src.shemas.doctors_schedule import *

router = APIRouter(prefix="/clinic", tags=["Врачи"])
    
@router.get("/{clinic_id}/doctors/{doctor_id}/bookings/")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()    

@router.get("/{clinic_id}/doctors/{doctor_id}/schedule")
async def get_schedule(db: DBDep):
    return await db.doctorsSchedule.get_all()   

@router.get("/{clinic_id}/doctors/{doctor_id}/schedule")
async def get_schedule_clinics(db: DBDep):
    return await db.doctorsSchedule.get_all()   

@router.get("/{clinic_id}/doctors")
async def get_doctors(db: DBDep):
    return await db.doctors.get_all()

@router.get("/clinic_id/doctors/{doctor_id}")
async def get_doctors_by_id(db: DBDep, doctor_id: int = Path()):
    return await db.doctors.get_filtred(id=doctor_id)

@router.post("/{clinic_id}/doctors/{doctor_id}")
async def add_doctor(db: DBDep,user_id:UserDependecies, data: DoctorRequestAdd = Body(), clinic_id: int = Path()):
    user_data = await db.users.get_one_or_none(id=user_id)
    if user_data.role == "admin":
        add_doctor_data = DoctorAdd(clinic_id=clinic_id, **data.model_dump())
        res = await db.doctors.add_one(add_doctor_data)
        await db.commit()
        return res
    return {"status":"error", "message":"нет прав"}

@router.post("/{clinic_id}/doctors/{doctor_id}/bookings/")
async def add_booking(
    db: DBDep,
    
    booking_data: BookingRequestAdd,
    user_id: UserDependecies,
    doctor_id: int = Path()
):
    service = BookingService(db)
    time = await service.check_availability(
        doctor_id,
        booking_data.date
    )

    booking_dict = booking_data.model_dump()
    booking_dict['user_id'] = user_id
    booking_dict['doctor_id'] = doctor_id

    if booking_data.date:
        booking_dict['date'] = booking_data.date
    else:
        booking_dict['date'] = time

    add_booking_data = BookingAdd(**booking_dict)
    res = await db.bookings.add_one(add_booking_data)
    await db.commit()
    return {"status": "ok", "data": res}

@router.post("/{clinic_id}/doctors/{doctor_id}/schedule")
async def add_schedule(
    db: DBDep,
    user_id: UserDependecies,
    data: ScheduleRequestAdd,
    doctor_id: int = Path(),
    clinic_id: int = Path()
    ):
    user_data = await db.users.get_one_or_none(id=user_id)
    if user_data.role == "admin":
        add_schedule_data = ScheduleAdd(
            doctor_id=doctor_id,
            clinic_id=clinic_id,
            **data.model_dump()
        )
        res = await db.doctorsSchedule.add_one(add_schedule_data)
        await db.commit()
        return res
    return {"status":"error", "message":"нет прав"}
    
@router.put("/{clinic_id}/doctors/{doctor_id}/schedules/{schedule_id}")
async def update_schedule(
    db: DBDep,
    user_id: UserDependecies,
    data: ScheduleRequestAdd,  # Отдельная модель для обновления (может иметь опциональные поля)
    doctor_id: int = Path(),
    clinic_id: int = Path(),
    schedule_id: int = Path()
):
    user_data = await db.users.get_one_or_none(id=user_id)
    if user_data.role == "admin":
        update_data = ScheduleAdd(
            clinic_id=clinic_id,
            doctor_id=doctor_id,
            **data.model_dump()
        )
        old_schedule = await db.doctorsSchedule.get_one_or_none(id=schedule_id)
        await db.doctorsSchedule.edit(update_data, id=schedule_id)
        
        booking_service = BookingService(db)
        await booking_service.reschedule_bookings(
            doctor_id,
            old_schedule,
            update_data
        )
        
        
        await db.commit()
        return {"status":"ok"}
    return {"status":"error", "message":"нет прав"}

# Эндпоинт для удаления расписания (DELETE)
@router.delete("/{clinic_id}/schedules/{schedule_id}")
async def delete_schedule(
    db: DBDep,
    user_id:UserDependecies,
    schedule_id: int = Path()
):
    user_data = await db.users.get_one_or_none(id=user_id)
    if user_data.role == "admin":
        data = await db.doctorsSchedule.get_one_or_none(id=schedule_id)
        doctor_id = data.id
        # await db.doctorsSchedule.delete(id=schedule_id)
        booking_service = BookingService(db)
        
        await booking_service.handle_schedule_change(doctor_id, schedule_id)
        await db.commit()
        return {"status": "success", "message": "Schedule deleted"}
    return {"status":"error", "message":"нет прав"}