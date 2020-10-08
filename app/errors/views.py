from app import db
from flask import render_template
from . import errors


@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('errors/500.html'), 500
