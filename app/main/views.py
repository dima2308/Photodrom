from . import main
from flask import render_template
from app.models import User, Photo
from flask_login import login_required, current_user


@main.route('/profile')
@login_required
def profile():
    user = User.query.filter(User.user_id == current_user.user_id).first()
    photos = Photo.query.filter(Photo.author_id == current_user.user_id).order_by(
        Photo.count_likes.desc())

    return render_template('main/profile.html', user=user, photos=photos)


@main.route('/')
def index():
    photo = Photo.query.order_by(Photo.count_likes.desc()).first()
    return render_template('main/index.html', photo=photo)
