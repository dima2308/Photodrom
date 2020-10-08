from flask import Blueprint

photos = Blueprint('photos', __name__, template_folder='templates')

from . import views