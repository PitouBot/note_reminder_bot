import re
from datetime import datetime, timedelta

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
    
    # Сначала проверяем "через IN"
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