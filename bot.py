import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import help, admin, notes, start
from database import init_db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

init_db()

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(help.router)
dp.include_router(admin.router)
dp.include_router(notes.router)
dp.include_router(start.router)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
