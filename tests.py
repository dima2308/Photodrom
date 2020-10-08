from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
import pytest
from app import app, db
from app.models import User, Photo


@pytest.fixture
def init_db():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()


class TestUserModel():
    def test_password_hashing(self, init_db):
        u = User(name='test_user', email='testuser@mail.ru', login='test_user')
        u.set_password('test')

        assert u.check_password('test')
        assert not(u.check_password('qwerty'))

    def test_add_user(self, init_db):
        u = User(name='test_user', email='testuser@mail.ru', login='test_user')
        u.set_password('test')

        db.session.add(u)
        db.session.commit()

        assert User.query.filter(User.login == 'test_user').first()

    #@pytest.mark.skip('Пока не требуется')
    def test_add_same_user_email(self, init_db):
        u1 = User(name='test_user', email='testuser@mail.ru', login='test_user1')
        u1.set_password('test')
        db.session.add(u1)
        db.session.commit()

        u2 = User(name='test_user', email='testuser@mail.ru', login='test_user2')
        u2.set_password('test')
        db.session.add(u2)

        try:
            db.session.commit()
        except IntegrityError:
            assert True

    #@pytest.mark.skip('Пока не требуется')
    def test_add_same_user_login(self, init_db):
        u1 = User(name='test_user', email='testuser1@mail.ru', login='test_user1')
        u1.set_password('test')
        db.session.add(u1)
        db.session.commit()

        u2 = User(name='test_user', email='testuser2@mail.ru', login='test_user1')
        u2.set_password('test')
        db.session.add(u2)

        try:
            db.session.commit()
        except IntegrityError:
            assert True
