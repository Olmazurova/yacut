from datetime import datetime

from . import db


class URLMap(db.Model):
    """Модель описывает короткую ссылку."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
