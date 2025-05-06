# src/service/BookingService.py
from datetime import datetime, timedelta
from fastapi import HTTPException
from src.shemas.booking import *
from src.api.dependencies import DBDep

class BookingService:
    def __init__(self, db: DBDep):
        self.db = db
    
    async def check_availability(self, doctor_id: int, booking_time: datetime | None):
        if booking_time is None:
            schedules = await self.db.doctorsSchedule.get_all()
            for schedule in schedules:
                existing = await self.db.bookings.get_filtred(
                    doctor_id=doctor_id,
                    date_from=schedule.start_time,
                    date_to=schedule.end_time
                )

                current_time = schedule.start_time
                while current_time < schedule.end_time:
                    is_available = True
                    for booking in existing:
                        if abs((booking.date - current_time).total_seconds()) < 3600:
                            is_available = False
                            break

                    if is_available:
                        booking_time = current_time
                        break

                    # Перемещаемся на 1 час вперед
                    current_time += timedelta(hours=1)

                if booking_time:
                    break
        if not booking_time:
            raise HTTPException(400, "Нет доступного времени для записи")

        schedule = await self.db.doctorsSchedule.get_current_schedule(
            doctor_id, 
            booking_time
        )
        
        if not schedule:
            raise HTTPException(400, "Врач не работает в это время")
        
        existing = await self.db.bookings.get_filtred(doctor_id=doctor_id)
        for booking in existing:
            if abs((booking.date - booking_time).total_seconds()) < 3600:
                raise HTTPException(400, "Минимальный интервал - 1 час")
        return booking_time


    async def reschedule_bookings(self, doctor_id: int, old_schedule, new_schedule):
        bookings = await self.db.bookings.get_filtred(
            doctor_id=doctor_id,
            date_from=old_schedule.start_time,
            date_to=old_schedule.end_time
        )

        # Рассчитываем разницу между новым и старым расписанием
        time_diff = new_schedule.start_time - old_schedule.start_time

        # Обновляем время бронирований
        for booking in bookings:
            new_time = booking.date + time_diff
            
            # Проверяем доступность нового времени
            try:
                new_data = BookingUpdateTime(date=new_time)
                await self.check_availability(doctor_id, new_time)
                await self.db.bookings.edit(
                    new_data,
                    exclude_unset=True,
                    id = booking.id
                )
                await self.db.commit()
            except HTTPException:
                # Если время занято, отменяем бронь
                await self.db.bookings.delete(id=booking.id)
                # Здесь можно добавить уведомление пользователю
                
    async def handle_schedule_change(self, doctor_id: int, schedule_id: int):
        # Получаем удаляемое/изменяемое расписание
        target_schedule = await self.db.doctorsSchedule.get_one_or_none(id=schedule_id)
        print(f"DJSJJJJJJJJJJJJJJJJJJJJJJJ{target_schedule.start_time}")
        # Находим все брони врача в период действия этого расписания
        bookings = await self.db.bookings.get_filtred(
            doctor_id=doctor_id,
            date_from=target_schedule.start_time,
            date_to=target_schedule.end_time
        )

        # Получаем другие активные расписания врача
        other_schedules = await self.db.doctorsSchedule.get_filtred(doctor_id=doctor_id)
        # other_schedules.remove(target_schedule)
        for booking in bookings:
            new_slot = None
            best_candidate = None
            
            # Ищем подходящий слот в других расписаниях
            for schedule in other_schedules:

                new_time = booking.date.replace(
                    month=schedule.start_time.month,
                    day=schedule.start_time.day,
                    hour=schedule.start_time.hour,
                    minute=schedule.start_time.minute
                )
                
                # Проверяем доступность
                try:
                    await self.check_availability(doctor_id, new_time)
                    new_slot = new_time
                    best_candidate = schedule
                    break
                except HTTPException:
                    continue

            if new_slot and best_candidate:
                new_data = BookingUpdateTime(date=new_time)
                await self.db.bookings.edit(
                    new_data,
                    id=booking.id
                )
                await self.db.commit()
            else:
                # Отменяем бронь если не нашли слот
                await self.db.bookings.delete(id=booking.id)
                # Добавить логику уведомления

        # Удаляем/обновляем само расписание
        await self.db.doctorsSchedule.delete(id=schedule_id)
        await self.db.commit()