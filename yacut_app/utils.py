from random import choices, randrange
from string import ascii_letters, digits

CHARS = list(ascii_letters + digits)


def get_unique_short_id():
    """Формирует короткий индикатор для ссылки переменной длины."""
    return choices(CHARS, k=randrange(4,16))
