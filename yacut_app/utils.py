from random import choices
from string import ascii_letters, digits

CHARS = list(ascii_letters + digits)
LENGTH_SHORT_ID = 6


def get_unique_short_id():
    """Формирует короткий индикатор для ссылки."""
    return choices(CHARS, k=LENGTH_SHORT_ID)


async def upload_file_and_get_url(session, file):
    """Загружает файлы на Яндекс Диск и получает на них ссылки."""
    pass


async def async_upload_files_to_ya_disk(files):
    """Создаёт задачи по количеству загруженных файлов."""
    pass
