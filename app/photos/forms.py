from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import Category


class PhotoForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    description = TextAreaField("Описание", validators=[
        DataRequired(),
        Length(min=3, max=128, message='Описание должно содержать от 5 до 255 символов')]
    )
    url = StringField("URL", validators=[DataRequired()])
    category = SelectField("Категория", choices=[
                           cat for cat in Category.query.all()], validators=[DataRequired()])


class CommentForm(FlaskForm):
    body = TextAreaField("Комментарий", validators=[
        DataRequired(message='Заполните поле'),
        Length(min=5, max=100, message='Комментарий должен содержать от 5 до 100 символов')]
    )
