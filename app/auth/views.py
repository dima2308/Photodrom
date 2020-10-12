from app import db
from . import auth
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, Photo
from app.utils import send_mail
from faker import Faker
from .forms import LoginForm, RegistrationForm, ForgotForm, ChangePasswordForm


@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/'))

    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        form_email = request.form.get('email')
        form_password = request.form.get('password')

        user = db.session.query(User).filter(User.email == form_email).first()

        if user:
            if user.check_password(form_password):
                login_user(user)
                return redirect('/')
            else:
                flash("Неверный пароль")
        else:
            flash("Пользователя с данным email не существует")

    return render_template('auth/login.html', form=form)


@auth.route('/registration', methods=["GET", "POST"])
def registration():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate_on_submit():
        form_name = request.form.get('name')
        form_login = request.form.get('login')
        form_email = request.form.get('email')
        form_password = request.form.get('password')

        user_email = db.session.query(User).filter(
            User.email == form_email).first()
        user_login = db.session.query(User).filter(
            User.email == form_login).first()

        if user_email:
            flash('Пользователь с данным email уже существует')
            return render_template('auth/registration.html', form=form)

        if user_login:
            flash('Пользователь с данный login уже существует')
            return render_template('auth/registration.html', form=form)

        new_user = User(name=form_name, login=form_login, email=form_email)
        new_user.set_password(form_password)

        db.session.add(new_user)
        db.session.commit()
        send_mail('Регистрация на сайте Photodrom', user.email,
                  'mail/registration_mail.html', name=user.name)

        return redirect(url_for('login'))

    return render_template('auth/registration.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter(
            User.email == request.form.get('email')).first()
        if user:
            faker = Faker()
            new_password = faker.password()
            user.set_password(new_password)
            db.session.commit()
            send_mail('Восстановление пароля', user.email,
                      'mail/recovery_password.html', name=user.name, password=new_password)

            return redirect(url_for('index'))

        else:
            flash("Пользователя с данным email не существует")
            return render_template('auth/forgot.html', form=form)

    return render_template('auth/forgot.html', form=form)


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter(User.email == current_user.email).first()

        if user.check_password(request.form.get('old_password')):
            user.set_password(request.form.get('new_password'))
            db.session.commit()
            return redirect('/')
        else:
            flash('Неверный текущий пароль')
            return render_template('auth/change_password.html', form=form)

    return render_template('auth/change_password.html', form=form)
