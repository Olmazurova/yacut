from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import FileForm, LinkForm
from .models import URLMap
from .utils import get_unique_short_id, async_upload_files_to_ya_disk

URL_HOST = 'http://127.0.0.1:5000/'
SHORT_PREFIX = 'short/'

@app.route('/', methods=['GET', 'POST'])
def generate_short_link_view():
    """Представление для генерации короткой ссылки."""
    form = LinkForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        short_id_list = URLMap.query.with_entities(URLMap.short).all()
        if short_id in short_id_list.append('files'):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('get_link.html', form=form)
        if short_id is None:
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
        return redirect(
            url_for('get_link.html', short_link=short_link),
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
        links = [
            URLMap(original=url[0], short=url[1])
            for url in urls
        ]
        db.session.add_all(links)
        db.session.commit()
        return redirect(
            url_for('add_files.html', links=links),
        )
    return render_template('add_files.html', form=form)
