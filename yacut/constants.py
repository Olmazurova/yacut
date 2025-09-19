from string import ascii_letters, digits

from . import app

CHARS = list(ascii_letters + digits)
LENGTH_SHORT_ID = 6

URL_HOST = 'http://localhost/'
SHORT_PREFIX = 'short/'

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
AUTH_HEADERS = {'Authorization': f'OAuth {app.config['DISK_TOKEN']}'}
