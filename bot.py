import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handlers import start, help, admin, echo

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(start.router)
dp.include_router(help.router)
dp.include_router(admin.router)
dp.include_router(echo.router)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
