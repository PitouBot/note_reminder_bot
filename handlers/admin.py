import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from config import ADMINS
from database import reset_table, get_stats
from keyboards import admin_menu, reset_keyboard

router = Router()
logger = logging.getLogger(__name__)


def is_admin(user_id: int) -> bool:
    return user_id in ADMINS


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("У вас нет доступа к этой команде.")
        return
    
    await message.answer(
        "👑 *Админ-панель*\n\n"
        "Выберите действие:",
        parse_mode="Markdown",
        reply_markup=admin_menu
    )


@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    await callback.answer()

    if not is_admin(callback.from_user.id):
        await callback.message.edit_text("⛔️ Доступ запрещён.")
        return

    stats = get_stats()
    
    text = f"📊 *Статистика бота*\n\n"
    text += f"👤 Всего пользователей: {stats['total_users']}\n"
    text += f"📝 Всего заметок: {stats['total_notes']}\n"
    text += f"⏰ Активных напоминаний: {stats['active_reminders']}\n\n"

    await callback.message.edit_text(text, parse_mode="Markdown", reply_markup=admin_menu)


@router.callback_query(F.data == "admin_reset_table")
async def admin_reset_table_prompt(callback: CallbackQuery):
    await callback.answer()
    
    if not is_admin(callback.from_user.id):
        return
        
    await callback.message.edit_text(
        "⚠️ *ВНИМАНИЕ!*\n\n"
        "Таблица `notes` будет УДАЛЕНА и создана заново.\n"
        "Это удалит ВСЕ данные и сбросит ID на 1.\n\n"
        "Вы уверены?",
        parse_mode="Markdown",
        reply_markup=reset_keyboard
    )


@router.callback_query(F.data == "admin_reset_confirm")
async def admin_reset_confirm(callback: CallbackQuery):
    await callback.answer()
    
    if not is_admin(callback.from_user.id):
        return
    
    # Удаляем и пересоздаём таблицу
    reset_table()
    
    await callback.message.edit_text(
        "✅ Таблица `notes` пересоздана!\n\n"
        "Теперь ID начинаются с 1.",
        reply_markup=admin_menu
    )


@router.callback_query(F.data == "admin_cancel")
async def admin_cancel(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "❌ Действие отменено.",
        reply_markup=admin_menu
    )














