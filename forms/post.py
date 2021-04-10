from flask_wtf import FlaskForm

from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms import BooleanField, SelectMultipleField

from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class CreatePostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    slug = StringField('Ссылка')
    tags = SelectMultipleField("Теги")
    submit = SubmitField('Применить')

class DeletePostForm(FlaskForm):
    submit = SubmitField('Удалить')

class EditPostForm(FlaskForm):
    # код одинаковый с созданием, но если редактирование будет проходить
    # иначе чем создание этот класс имеет смысл
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    slug = StringField('Ссылка')
    tags = SelectMultipleField("Теги")
    submit = SubmitField('Применить')
