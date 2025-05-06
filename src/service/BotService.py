from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
import asyncio  # Добавляем импорт asyncio

# Ваш остальной код...

from src.api.dependencies import DBDep
from src.config import settings


class Botclass:
    def __init__(self, token: str):
        self.bot = Bot(token=token)
        self.dp = Dispatcher(self.bot)
    async def check_appointments(self):
        today = date.today()
        appointments = DBDep.bookings.get_all()
        for appointment in appointments:
            message = (
                f"🔔 Напоминание о записи к ветеринару!\n"
                f"🕒 Дата: {appointment.date}"
            )
            if appointment.date == today:
                await self.bot.send_message(appointment.tg_username, message)
                
    async def on_startup(self, dp):
        await self.check_appointments()
    
    def start(self):
        executor.start_polling(
            self.dp, 
            skip_updates=True,
            on_startup=self.on_startup
        )

bot = Botclass(token="7667372068:AAGflrdiwbs16xBeQdliZsHQ8hifSSOvYF8")

@Botclass.dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать! Бот будет присылать уведомления о записях.")
    
async def main():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    # Регистрация обработчиков
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(add_appointment, Command("add"))
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())