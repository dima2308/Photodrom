from . import app
from .models import *
from flask_login import current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect


class AdminMixin:
    def is_accessible(self):
        return 'Admin' in current_user.roles

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/')


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class PhotoAdminView(AdminMixin, ModelView):
    form_columns = ['title', 'description', 'url', 'category']


class UserAdminView(AdminMixin, ModelView):
    form_columns = ['name', 'email', 'login', 'password_hash', 'roles']


class CommentAdminView(AdminMixin, ModelView):
    form_columns = ['body', 'photo', 'user_comment']


class CategoryAdminView(AdminMixin, ModelView):
    form_columns = ['name']


admin = Admin(app, 'Photodrom', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PhotoAdminView(Photo, db.session))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(CommentAdminView(Comment, db.session))
admin.add_view(CategoryAdminView(Category, db.session))
