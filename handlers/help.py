import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards import main_menu

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Доступные команды:\n/start - приветствие\n/help - помощь\n/all_notes - показать все заметки\n"
        "Для дополнительных функций можно использовать информативную клавиатуру бота",
        reply_markup=main_menu
    )

@router.callback_query(F.data == 'help')
async def cmd_help(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "Доступные команды:\n/start - приветствие\n/help - помощь\n/all_notes - показать все заметки\n"
        "Для дополнительных функций можно использовать информативную клавиатуру бота",
        reply_markup=main_menu
    )