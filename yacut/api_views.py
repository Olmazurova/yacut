from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id, validate_custom_id, get_short_id_list


@app.route('/api/id', methods=['POST'])
def generate_short_link():
    """Генерирует короткую ссылку взамен отправленной."""
    if not request.data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    # я бы проверяла есть ли в базе оригинальная ссылка и
    # если есть возвращала бы её короткую ссылку
    # (невзирая на то передан короткий вариант или нет), но тесты не проходят.
    # link = URLMap.query.filter_by(original=data['url']).first()
    # if link is not None:
    #     return jsonify(link.to_dict()), HTTPStatus.OK
    if 'custom_id' not in data or data['custom_id'] == '':
        short_id = get_unique_short_id()
    else:
        short_id = data['custom_id']
        if not validate_custom_id(short_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if short_id in get_short_id_list():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    link = URLMap(original=data['url'], short=short_id)
    db.session.add(link)
    db.session.commit()
    return jsonify(link.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/')
def get_original_link(short_id):
    """Возвращает оригинальную ссылку связанную с короткой ссылкой."""
    link = URLMap.query.filter_by(short=short_id).first()
    print('short_link', link)
    if link is not None:
        return jsonify({'url': link.original}), HTTPStatus.OK
    raise InvalidAPIUsage(
        'Указанный id не найден', HTTPStatus.NOT_FOUND
    )
