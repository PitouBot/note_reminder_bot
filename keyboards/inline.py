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
        InlineKeyboardButton(text="❓ Помощь", callback_data="help")
    ],
])

