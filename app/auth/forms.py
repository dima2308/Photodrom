from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
                        Email('Некорректный email'), DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    login = StringField("Логин", validators=[DataRequired()])
    email = StringField("Email", validators=[
                        Email('Некорректный email'), DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired(), EqualTo('confirm',
                                                                           message="Пароли не совпадают")])
    confirm = PasswordField("Пароль (ещё раз)", validators=[DataRequired()])


class ForgotForm(FlaskForm):
    email = StringField("Email", validators=[
                        Email('Некорректный email'), DataRequired()])


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Текущий пароль", validators=[DataRequired()])
    new_password = PasswordField("Новый пароль", validators=[DataRequired(), EqualTo('confirm',
                                                                           message="Пароли не совпадают")])
    confirm = PasswordField("Новый пароль (ещё раз)", validators=[DataRequired()])
