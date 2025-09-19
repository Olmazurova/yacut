from datetime import datetime

from . import db
from .constants import URL_HOST, SHORT_PREFIX


class URLMap(db.Model):
    """Модель описывает короткую ссылку."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    # file_name = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    def to_dict(self):
        return {'url': self.original,
                'short_link': f'{URL_HOST}{self.short}'}
