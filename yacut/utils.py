from random import choices
import urllib.parse

import aiohttp
import asyncio
import json

from .constants import (AUTH_HEADERS, CHARS, DOWNLOAD_LINK_URL,
                        LENGTH_SHORT_ID, REQUEST_UPLOAD_URL, SHORT_PREFIX,
                        URL_HOST)
from .models import URLMap

def get_short_id_list():
    short_id_list = [short[0]
                     for short
                     in URLMap.query.with_entities(URLMap.short).all()]
    short_id_list.append('files')
    return short_id_list


def get_unique_short_id():
    """Формирует короткий индикатор для ссылки."""
    short_id_list = get_short_id_list()
    short_id = ''.join(choices(CHARS, k=LENGTH_SHORT_ID))
    while short_id in short_id_list:
        short_id = ''.join(choices(CHARS, k=LENGTH_SHORT_ID))
    return short_id


def validate_custom_id(custom_id):
    """Проверяет, что короткая ссылка пользователя удовлетворяет условиям."""
    print(len(custom_id))
    if len(custom_id) not in range(1, 17):
        return False
    if set(custom_id) - set(CHARS):
        return False
    return True


async def get_temporary_link(session, file_name):
    """Получает от Яндекс Диска временную ссылку для загрузки файла."""
    payload = {
        'path': f'app:/{file_name}',
        'overwrite': 'True'
    }
    response = await session.get(
        headers=AUTH_HEADERS,
        params=payload,
        url=REQUEST_UPLOAD_URL
    )
    json_response = await response.json()
    return json_response['href']


async def upload_file_and_get_url(session, file):
    """Загружает файлы на Яндекс Диск и получает на них ссылки."""
    upload_url = await get_temporary_link(session, file.filename)
    file_data = file.read()
    async with session.put(
        data=file_data,
        url=upload_url,
    ) as response:
        location = response.headers['Location']
        location = urllib.parse.unquote(location)

        location = location.replace('/disk', '')

    async with session.get(
        headers=AUTH_HEADERS,
        url=DOWNLOAD_LINK_URL,
        params={'path': location}
    ) as response:
        json_response = await response.json()
        original_link = json_response['href']
    short_id = get_unique_short_id()
    return {'original_link': original_link, 'short_id': short_id}


async def async_upload_files_to_ya_disk(files):
    """Создаёт задачи по количеству загруженных файлов."""
    tasks = []
    async with aiohttp.ClientSession() as session:
        for file in files:
            tasks.append(
                asyncio.ensure_future(
                    upload_file_and_get_url(session, file)
                )
            )
        urls = await asyncio.gather(*tasks)
    return urls
