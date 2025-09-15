from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileSize
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class LinkForm(FlaskForm):
    """Форма для создания короткой ссылки."""

    original_link = URLField(
        'Введите ссылку, которую нужно сократить',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = URLField(
        'Введите короткую ссылку, которую хотите установить',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')


class FileForm(FlaskForm):
    """Форма для загрузки файлов на Яндекс Диск и получения ссылки на них."""

    files = MultipleFileField(
        validators=[FileSize(
            20_000_000,
            message='Размер файла не может быть больше 20 Mb.'
        )],
    )
    submit = SubmitField('Загрузить')
