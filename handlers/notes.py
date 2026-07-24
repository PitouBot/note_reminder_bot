import logging
import re
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import NoteForm
from keyboards import main_menu
from datetime import datetime, timedelta
from database import save_note, show_all_notes, get_notes_by_name, delete_note


router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data == 'make_note')
async def make_note(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(NoteForm.note_name)
    logger.info(f"Состояние установлено: {await state.get_state()}") 
    await callback.message.edit_text(
        "Напишите запоминающееся название заметки",
        reply_markup=main_menu
    )


@router.message(NoteForm.note_name)
async def save_note_name(message: Message, state: FSMContext):
    await state.update_data(note_name=message.text.strip())

    await state.set_state(NoteForm.note_text)
    logger.info(f"Состояние установлено: {await state.get_state()}") 


    await message.answer(
        'Напишите текст вашей заметки',
        reply_markup=main_menu
    )


@router.message(NoteForm.note_text)
async def save_note_text(message: Message, state: FSMContext):
    await state.update_data(note_text=message.text.strip())

    await state.set_state(NoteForm.note_remind_time)
    logger.info(f"Состояние установлено: {await state.get_state()}") 


    await message.answer(
        "⏰ Укажите, **когда напомнить** о заметке.\n\n"
        "Примеры:\n"
        "• `сегодня 18:00`\n"
        "• `завтра 10:30`\n"
        "• `через 2 часа`\n"
        "• `2025-07-25 15:00`\n\n"
        "Если напоминание не нужно, отправьте 'skip', 'пропустить' или '-'",
        parse_mode="Markdown"
    )


@router.message(NoteForm.note_remind_time)
async def save_remind_time(message: Message, state: FSMContext):
    text = message.text.strip()

    if text in ("пропустить", "skip", "-", "нет"):
        remind_at = None
    else:
        remind_dt = parse_remind_time(text)
        if not remind_dt:
            await message.answer(
                "❌ Неправильный формат времени.\n\n"
                "Примеры:\n"
                "• `сегодня 18:00`\n"
                "• `завтра 10:30`\n"
                "• `через 2 часа`\n"
                "• `2025-07-25 15:00`\n\n"
                "Или отправьте `пропустить`, чтобы не устанавливать напоминание."
            )
            return
        remind_at = remind_dt.strftime("%Y-%m-%d %H:%M:%S")

    await state.update_data(note_remind_time=remind_at)

    data = await state.get_data()

    new_note_id = save_note(message.from_user.id, data.get('note_name'), data.get('note_text'), data.get('note_remind_time'))
   
    await message.answer(
        f'Ваша заметка была успешно сохранена в базе данных c id = {new_note_id}.\n'
        'Вы можете увидеть все ваши заметки по команде /all_notes'
    )

    await state.clear()


@router.callback_query(F.data == 'show_note')
async def show_note_prompt(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(NoteForm.searching_note)
    await callback.message.edit_text(
        "🔎 Введите название заметки (или его часть):",
        reply_markup=main_menu
    )

@router.message(NoteForm.searching_note)
async def search_note_by_name(message: Message, state: FSMContext):
    search_term = message.text.strip()

    notes = get_notes_by_name(message.from_user.id, search_term)

    if not notes:
        await message.answer(
            f"❌ Заметок с названием «{search_term}» не найдено.\n\n"
            "Попробуйте другое ключевое слово или создайте новую заметку.",
            reply_markup=main_menu
        )
        await state.clear()
        return

    text = f"🔍 *Найдено {len(notes)} заметок* по запросу «{search_term}»:\n\n"
    for note in notes[:10]:  # первые 10
        note_id, note_name, note_text, created_at, remind_at = note
        text += f"*📌 {note_name}* (ID: `{note_id}`)\n {note_text}\n"
        if remind_at:
            text += f"   ⏰ Напоминание: {remind_at}\n"
        text += "\n"
    
    if len(notes) > 10:
        text += f"... и ещё {len(notes) - 10} заметок."
    
    await message.answer(text, parse_mode="Markdown", reply_markup=main_menu)
    await state.clear()

@router.callback_query(F.data == 'show_all_notes')
@router.message(Command('all_notes'))
async def get_all_notes(event: Message | CallbackQuery):
    # Обработчик работает и для команды /all_notes, и для кнопки 'show_all_notes. Определяем, кто прислал запрос'
    if isinstance(event, Message):
        user_id = event.from_user.id
        answer_func = event.answer
    else:  # CallbackQuery
        await event.answer()  # обязательно убираем часики
        user_id = event.from_user.id
        answer_func = event.message.edit_text

    notes = show_all_notes(user_id)

    if not notes:
        await answer_func(
            f"❌ У вас нет заметок!\n\n",
            reply_markup=main_menu
        )
        return
    
    text = f"🔍 *Количество ваших заметок = {len(notes)} шт* »:\n\n"
    for note in notes:  
        note_id, note_name, note_text, created_at, remind_at = note
        text += f"*📌 {note_name}* (ID: `{note_id}`)\n {note_text}\n"
        if remind_at:
            text += f"   ⏰ Напоминание: {remind_at}\n"
        text += "\n"
       
    await answer_func(text, parse_mode="Markdown", reply_markup=main_menu)

@router.callback_query(F.data == 'delete_note')
async def del_note_prompt(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(NoteForm.note_id_for_deleting)
    await callback.message.edit_text(
        "🔎 Введите id заметки, которую хотите удалить",
        reply_markup=main_menu
    )

@router.message(NoteForm.note_id_for_deleting)
async def del_note(message: Message, state: FSMContext):
    id = message.text.strip()
    if not id.isdigit():
        await message.answer(
            f"❌ Неправильный ввод!ID должно быть целом числом\n\n",
            reply_markup=main_menu
        )
        return    

    success = delete_note(int(id), message.from_user.id)

    if success:
        await message.answer(
            f'✅ Заметка с id {id} была успешно удалена', 
            reply_markup=main_menu
        )
    else:
        await message.answer(
            f"❌ Заметка с ID {id} не найдена.",
            reply_markup=main_menu
        )

    await state.clear()
        
       

### Парсер времени напоминания

def parse_remind_time(text: str) -> datetime | None:
    """
    Парсит текст с временем напоминания.
    Поддерживает:
    - сегодня 18:00
    - завтра 10:30
    - через 15 минут
    - через 2 часа
    - через 3 дня
    - 2025-07-25 15:00
    - 25.07.2025 15:00
    - 25.07 15:00
    """
    text = text.lower().strip()
    now = datetime.now()
    
    # Сначала проверяем "через N"
    match = re.search(r'через\s+(\d+)\s+(минут(?:ы|у)?|час(?:а|ов)?|день|дня|дней)', text)
    if match:
        num = int(match[1])
        unit = match[2]
        if 'минут' in unit:
            return now + timedelta(minutes=num)
        elif 'час' in unit:
            return now + timedelta(hours=num)
        elif 'день' in unit or 'дня' in unit or 'дней' in unit:
            return now + timedelta(days=num)
    
    # Проверяем "сегодня", "завтра", "послезавтра"
    date_keywords = {
        'сегодня': 0,
        'завтра': 1,
        'послезавтра': 2
    }
    
    for keyword, days_offset in date_keywords.items():
        match = re.search(rf'{keyword}\s+(\d{{1,2}}):(\d{{2}})', text)
        if match:
            hour, minute = int(match[1]), int(match[2])
            target = (now + timedelta(days=days_offset)).replace(
                hour=hour, minute=minute, second=0, microsecond=0
            )
            return target if target > now else target + timedelta(days=1)
    
    # Проверяем дату в формате YYYY-MM-DD HH:MM
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})\s+(\d{1,2}):(\d{2})', text)
    if match:
        try:
            return datetime(int(match[1]), int(match[2]), int(match[3]), int(match[4]), int(match[5]))
        except ValueError:
            return None
    
    # Проверяем дату в формате DD.MM.YYYY HH:MM
    match = re.search(r'(\d{2})\.(\d{2})\.(\d{4})\s+(\d{1,2}):(\d{2})', text)
    if match:
        try:
            return datetime(int(match[3]), int(match[2]), int(match[1]), int(match[4]), int(match[5]))
        except ValueError:
            return None
    
    # Проверяем дату в формате DD.MM HH:MM (без года)
    match = re.search(r'(\d{2})\.(\d{2})\s+(\d{1,2}):(\d{2})', text)
    if match:
        try:
            return datetime(now.year, int(match[2]), int(match[1]), int(match[3]), int(match[4]))
        except ValueError:
            return None
    
    return None