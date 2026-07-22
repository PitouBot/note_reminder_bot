from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import NoteForm
from keyboards import main_menu
# from database import save_note 


router = Router()


@router.callback_query(F.data == 'make_note')
async def make_note(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(NoteForm.note)
    await callback.message.edit_text(
        "Напишите заметку и бот сохранит ее для вас в базе данных",
        reply_markup=main_menu
    )

@router.message(NoteForm.note)
async def save_note(message: Message, state: FSMContext):
    await state.update_data(note=message.text.strip())

    data = await state.get_data()

    await message.answer(
        'Ваша заметка была успешно сохранена в базе данных. '
        'Вы можете увидить все ваши заметки по команде /all_notes'
    )

    # new_note = save_note(data)

    # await state.clear()