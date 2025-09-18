import urllib.parse

from flask import flash, redirect, render_template, url_for

from . import app, db
from .constants import URL_HOST, SHORT_PREFIX
from .forms import FileForm, LinkForm
from .models import URLMap
from .utils import get_unique_short_id, async_upload_files_to_ya_disk


@app.route('/', methods=['GET', 'POST'])
def generate_short_link_view():
    """Представление для генерации короткой ссылки."""
    form = LinkForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        print('Short', short_id)
        short_id_list = ['files'] + URLMap.query.with_entities(
            URLMap.short
        ).all()
        if short_id in short_id_list:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('get_link.html', form=form)
        if short_id == '':
            short_id = get_unique_short_id()
            while short_id in short_id_list:
                short_id = get_unique_short_id()
        link = URLMap(
            original=form.original_link.data,
            short=short_id
        )
        db.session.add(link)
        db.session.commit()
        short_link = f'{URL_HOST}{SHORT_PREFIX}{link.short}'
        print('short_link', short_link)
        return render_template(
            'get_link.html', form=form, short_link=short_link
        )
    return render_template('get_link.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def add_files_view():
    """
    Представление для загрузки файлов на Яндекс Диск
    и получения сслыки на них.
    """
    form = FileForm()
    if form.validate_on_submit():
        urls = await async_upload_files_to_ya_disk(form.files.data)
        print(form.files.data, type(form.files.data))
        links = [
            URLMap(original=url['original_link'], short=url['short_id'])
            for url in urls
        ]
        db.session.add_all(links)
        db.session.commit()
        files = []
        for link in links:
            parsed_url = urllib.parse.urlparse(link.original)
            params = urllib.parse.parse_qs(parsed_url.query)
            filename_encoded = params.get('filename', [None])[0]  # Обработать ошибку если нет ключа
            files.append(
                (filename_encoded, f'{URL_HOST}{SHORT_PREFIX}{link.short}')
            )
        return render_template(
            'add_files.html', form=form, files=files
        )
    return render_template('add_files.html', form=form)


@app.route('/short/<string:short_id>/', methods=['GET', 'POST'])
def redirect_to_original_link_view(short_id):
    """Принимает короткую ссылку и перенаправляет на оригинальную."""
    original_link = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(original_link.original)  # почему при загрузке на яндекс диск не даёт доступ к файлам по ссылке? ошибка 403
