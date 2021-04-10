from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms import BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class CreateTagForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    slug = StringField('Ссылка')
    submit = SubmitField('Применить')

class DeleteTagForm(FlaskForm):
    submit = SubmitField('Удалить')

class EditTagForm(FlaskForm):
    # код одинаковый с созданием, но если редактирование будет проходить
    # иначе чем создание этот класс имеет смысл
    title = StringField('Заголовок', validators=[DataRequired()])
    slug = StringField('Ссылка')
    submit = SubmitField('Применить')
