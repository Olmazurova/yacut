from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id', methods=['POST'])
def generate_short_link():
    """Генерирует короткую ссылку взамен отправленной."""
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    link = URLMap.query.filter_by(original=data['url']).first()
    if link is not None:
        return jsonify(link.to_dict()), HTTPStatus.OK
    short_id = get_unique_short_id()
    link = URLMap(original=data['url'], short=short_id)
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/')
def get_original_link(short_id):
    """Возвращает оригинальную ссылку связанную с короткой ссылкой."""
    link = URLMap.query.filter_by(short=short_id).first()
    if link is not None:
        return jsonify({'url': link.original}), HTTPStatus.OK
    raise InvalidAPIUsage(
        'Указанный id не найден', HTTPStatus.NOT_FOUND
    )
