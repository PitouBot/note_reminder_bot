import sqlite3
import logging
from datetime import datetime

DB_PATH = "notes.db"

logger = logging.getLogger(__name__) 


def init_db():
    """Создаёт таблицу заметок при первом запуске"""
    with sqlite3.connect(DB_PATH) as conn:    
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                note_name TEXT NOT NULL,
                note_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                remind_at TIMESTAMP,
                is_reminded INTEGER DEFAULT 0
            )
        """)
        logger.info("База данных инициализирована")

def save_note(user_id: int, note_name: str, note_text: str, remind_at: str) -> int:
    """Сохраняет заметку и возвращает её ID"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO notes (user_id, note_name, note_text, remind_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, note_name, note_text, remind_at))

        note_id = cursor.lastrowid

        logger.info(f"Заметка #{note_id} сохранена для пользователя {user_id}")
        return note_id

def get_notes_by_name(user_id: int, search_term: str) -> list:
    """
    Ищет заметки по названию (частичное совпадение, без учёта регистра)
    Возвращает список заметок: [(id, note_name, note_text, created_at, remind_at), ...]
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
    
        cursor.execute("""
            SELECT id, note_name, note_text, created_at, remind_at
            FROM notes
            WHERE user_id = ? AND note_name LIKE ? COLLATE NOCASE
            ORDER BY created_at DESC
        """, (user_id, f"%{search_term}%"))
        
        return cursor.fetchall()        # возвращает список кортежей. Каждый кортеж — это одна строка из таблицы.

def show_all_notes(user_id: int) -> list:
    """Возвращает все заметки пользователя"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, note_name, note_text, created_at, remind_at
            FROM notes
            WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))
    
    return cursor.fetchall()

def delete_note(note_id: int, user_id: int) -> bool:
    """Удаляет заметку"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
            
        cursor.execute("""
            DELETE FROM notes
            WHERE id = ? AND user_id = ?
        """, (note_id, user_id))

    deleted = cursor.rowcount > 0
    
    return deleted

def clear_table(table_name: str) -> None:
    """Удаляет все записи из указанной таблицы"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name}")
   
        logger.info(f"Таблица {table_name} очищена")

