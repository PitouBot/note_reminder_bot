from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📝 Сделать заметку", callback_data="make_note")
    ],
    [
        InlineKeyboardButton(text="🔎 Найти и показать заметку", callback_data="show_note")
    ],
    [
        InlineKeyboardButton(text="📃 Показать все заметки", callback_data="show_all_notes")
    ],
    [
        InlineKeyboardButton(text="❓ Помощь", callback_data="help")
    ],
    [
        InlineKeyboardButton(text="🗑️ Удалить запись", callback_data='delete_note')
    ]
])

