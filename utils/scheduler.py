import asyncio
import logging
from datetime import datetime
from aiogram import Bot
from database import get_due_reminders, mark_reminder_sent

logger = logging.getLogger(__name__)

async def check_reminders(bot: Bot):
    """
    Фоновая задача: каждую минуту проверяет, не пора ли отправить напоминание.
    """
    while True:
        try:
            reminders = get_due_reminders()
            
            for note_id, user_id, note_name, note_text, remind_at in reminders:
                try:
                    await bot.send_message(
                        user_id,
                        f"⏰ *НАПОМИНАНИЕ!*\n\n"
                        f"📌 *{note_name}*\n"
                        f"{note_text}\n\n"
                        f"🆔 ID: `{note_id}`",
                        parse_mode="Markdown"
                    )
                    mark_reminder_sent(note_id)
                    logger.info(f"Напоминание #{note_id} отправлено пользователю {user_id}")
                except Exception as e:
                    logger.error(f"Ошибка отправки напоминания #{note_id}: {e}")
            
        except Exception as e:
            logger.error(f"Ошибка в планировщике напоминаний: {e}")
        
        await asyncio.sleep(60)  # Проверяем каждую минуту