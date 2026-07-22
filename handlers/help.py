from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Доступные команды:\n/start - приветствие\n/help - помощь")
