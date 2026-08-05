from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📝 Сделать заметку", callback_data="make_note")
    ],
    [
        InlineKeyboardButton(text="✏️ Редактировать заметку", callback_data="edit_note")
    ],
    [
        InlineKeyboardButton(text="🔎 Найти и показать заметку", callback_data="show_note")
    ],
    [
        InlineKeyboardButton(text="📃 Показать все заметки", callback_data="show_all_notes")
    ],
    [
        InlineKeyboardButton(text="⏰ Установить напоминание", callback_data="set_remind")
    ],
    [
        InlineKeyboardButton(text="🗑️ Удалить запись", callback_data='delete_note')
    ],
    [
        InlineKeyboardButton(text="🗑️ Удалить все записи", callback_data='delete_all_notes')
    ],
    [
        InlineKeyboardButton(text="❓ Помощь", callback_data="help")
    ],
])

admin_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
    ],
    [
        InlineKeyboardButton(text="🔄 Сбросить таблицу", callback_data="admin_reset_table")
    ],
])

reset_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚠️ ДА, сбросить таблицу", callback_data="admin_reset_confirm")],
        [InlineKeyboardButton(text="❌ Нет, отмена", callback_data="admin_cancel")]
    ])
