import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message
from dotenv import load_dotenv
from logging import FileHandler, WARNING, Formatter


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.TestingConfig')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

if app.debug == False:
    file_handler = FileHandler(app.config['LOGFILE'])
    file_handler.setLevel(WARNING)
    file_handler.setFormatter(Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))

    app.logger.addHandler(file_handler)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, авторизуйтесь'

mail = Mail(app)

from app.models import *

from app.admin import admin

from .photos import photos
from .auth import auth
from .errors import errors
from .main import main


app.register_blueprint(photos, url_prefix='/photos')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(main)
app.register_blueprint(errors)
