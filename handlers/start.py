import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards import main_menu


router = Router()
logger = logging.getLogger(__name__)

@router.message()
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот-блокнот-напоминатель =).\n"
        "📝 Выбери действие:",
        reply_markup=main_menu
    )