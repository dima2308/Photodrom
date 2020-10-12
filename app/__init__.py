import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail, Message
from flask_security import SQLAlchemyUserDatastore, Security
from dotenv import load_dotenv
from logging import FileHandler, WARNING, Formatter


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.TestingConfig')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

file_handler = FileHandler('errors.txt')
formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
file_handler.setLevel(WARNING)

app.logger.addHandler(file_handler)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, авторизуйтесь'

mail = Mail(app)

from app.models import *

admin = Admin(app)
admin.add_view(ModelView(Photo, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(Category, db.session))

from .photos import photos
from .auth import auth
from .errors import errors
from .main import main

app.register_blueprint(photos, url_prefix='/photos')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(main)
app.register_blueprint(errors)
