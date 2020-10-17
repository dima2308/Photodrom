from . import mail
from app import app
from .models import Photo
from flask import render_template
from flask_mail import Message
from threading import Thread


def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, recipient, template, **kwargs):
    msg = Message(
        subject, sender=app.config['MAIL_DEFAULT_SENDER'],  recipients=[recipient])
    msg.html = render_template(template,  **kwargs)
    thr = Thread(target=async_send_mail,  args=[app,  msg])
    thr.start()
    return thr


def sort_photos(param):
    if param == 'title':
        photos = Photo.query.order_by(Photo.title.desc())
    elif param == 'count_likes':
        photos = Photo.query.order_by(Photo.count_likes.desc())
    elif param == 'created_date':
        photos = Photo.query.order_by(Photo.created_date.desc())
    else:
        photos = Photo.query
    return photos
