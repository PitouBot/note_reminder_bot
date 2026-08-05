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
                note_name_lower TEXT NOT NULL,
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
            INSERT INTO notes (user_id, note_name, note_name_lower, note_text, remind_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, note_name, note_name.lower(), note_text, remind_at))

        note_id = cursor.lastrowid

        logger.info(f"Заметка #{note_id} сохранена для пользователя {user_id}")
        return note_id


def get_due_reminders() -> list:
    """
    Возвращает все напоминания, у которых наступило время,
    и которые ещё не были отправлены.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, user_id, note_name, note_text, remind_at
            FROM notes
            WHERE remind_at IS NOT NULL
            AND remind_at <= datetime('now', 'localtime')
            AND is_reminded = 0
        """)
        return cursor.fetchall()


def mark_reminder_sent(note_id: int):
    """Помечает напоминание как отправленное"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
    
        cursor.execute("""
            UPDATE notes
            SET is_reminded = 1
            WHERE id = ?
        """, (note_id,))
    
        logger.info(f"Напоминание #{note_id} помечено как отправленное")


def update_remind_time(note_id: int, user_id: int, remind_at: str) -> bool:
    """Устанавливает время напоминания для заметки"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
    
        cursor.execute("""
            UPDATE notes
            SET remind_at = ?, is_reminded = 0
            WHERE id = ? AND user_id = ?
        """, (remind_at, note_id, user_id))
    
        return cursor.rowcount > 0


def update_note(note_id: int, user_id: int, note_text: str) -> bool:
    """Изменяет текст заметки"""
    with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
        
            cursor.execute("""
                UPDATE notes
                SET note_text = ?
                WHERE id = ? AND user_id = ?
            """, (note_text, note_id, user_id))
        
            return cursor.rowcount > 0


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
            WHERE user_id = ? AND note_name_lower LIKE ?
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


def clear_user_notes(user_id: int) -> int:
    """Удаляет все заметки пользователя. Возвращает количество удалённых записей."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notes WHERE user_id = ?", (user_id,))
        deleted = cursor.rowcount
        conn.commit()
        return deleted

def reset_table() -> None:
    """
    Удаляет таблицу notes и создаёт заново.
    ID сбрасываются на 1.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS notes")
    
    # Пересоздаём таблицу через init_db()
    init_db()
    logger.info("Таблица notes пересоздана")


def get_stats() -> dict:
    """Возвращает статистику по базе данных"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Всего пользователей
        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM notes")
        total_users = cursor.fetchone()[0]
        
        # Всего заметок
        cursor.execute("SELECT COUNT(*) FROM notes")
        total_notes = cursor.fetchone()[0]
        
        # Активные напоминания
        cursor.execute("SELECT COUNT(*) FROM notes WHERE remind_at IS NOT NULL AND is_reminded = 0")
        active_reminders = cursor.fetchone()[0]
        
                
        return {
            "total_users": total_users,
            "total_notes": total_notes,
            "active_reminders": active_reminders,
        }


