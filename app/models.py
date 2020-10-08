from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask_security import RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash


photo_likes = db.Table(
    'photo_likes',
    db.Column('photo_id', db.Integer, db.ForeignKey('photo.photo_id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'))
)


user_roles = db.Table(
    'user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.role_id'))
)


class Photo(db.Model):
    photo_id = db.Column(db.Integer(), primary_key=True)
    author_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    category_id = db.Column(
        db.Integer(), db.ForeignKey('category.category_id'))
    title = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(128))
    url = db.Column(db.String(255), nullable=False)
    count_likes = db.Column(db.Integer(), default=0)
    created_date = db.Column(db.DateTime(), default=datetime.now)
    comments = db.relationship('Comment', backref='photo')
    likes = db.relationship('User', secondary=photo_likes,
                            backref=db.backref('liked_photos', lazy='dynamic'))

    def __repr__(self):
        return '<Photo_id: {}, title: {}>'.format(self.photo_id, self.title)


class Category(db.Model):
    category_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    photos = db.relationship('Photo', backref='category')

    def __repr__(self):
        return self.name


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    login = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.DateTime(), default=datetime.now)
    photos = db.relationship('Photo', backref='user')
    comments = db.relationship('Comment', backref='user_comment')
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy="dynamic"))

    def __repr__(self):
        return self.login

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.user_id


class Comment(db.Model):
    comment_id = db.Column(db.Integer(), primary_key=True)
    author_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    photo_id = db.Column(db.Integer(), db.ForeignKey('photo.photo_id'))
    body = db.Column(db.Text)
    created_date = db.Column(db.DateTime(), default=datetime.now)

    def __repr__(self):
        return '<Comment_id: {}, body: {}>'.format(self.comment_id, self.body)


class Role(db.Model, RoleMixin):
    role_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
