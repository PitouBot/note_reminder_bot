from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import ADMINS

router = Router()

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id in ADMINS:
        await message.answer("Добро пожаловать в админ-панель!")
    else:
        await message.answer("У вас нет доступа к этой команде.")
