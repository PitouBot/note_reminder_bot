from aiogram.fsm.state import State, StatesGroup

class NoteForm(StatesGroup):
    note_name = State()
    note_text = State()
    note_remind_time = State()
    searching_note = State() 
    note_id_for_deleting = State()
    set_remind_id = State()
    set_remind_time = State()
    
   