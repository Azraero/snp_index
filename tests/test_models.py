import unittest
import datetime
from flask import current_app
from app.auth.models import User
from app.app import create_app
from app.exetensions import db


class UserTestCase(unittest.TestCase):
    """User tests."""
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_create_user(self):
        user = User(username='cc', email='test@qq.com', password='123')
        user.save()

        me = User.query.filter_by(username='cc').first()
        self.assertTrue(user == me)

    def test_update_user(self):
        user = User(username='xs', email='test@qq.com', password='123')

        user.update(email='haha@test.com', password='050400')
        self.assertTrue(user.email == 'haha@test.com')
        self.assertTrue(user.verify_password('050400'))

    def test_delete_user(self):
        user = User(username='lxgui', email='lxgui@test.com', password='123')
        user.save()

        lxgui = User.query.filter_by(username='lxgui').first()
        lxgui.delete()

        self.assertTrue(User.query.filter_by(username='lxgui').first() is None)

    def test_password_hash(self):
        user = User(username='jx', email='jx@test.com', password='123')
        user.save()

        jx = User.query.filter_by(username='jx').first()
        self.assertTrue(jx.verify_password('123'))

    def test_token(self):
        user = User(username='test', email='test@test.com', password='123')
        user.save()

        token = user.generate_confirmation_token()
        user.confirm(token)

        self.assertTrue(user.is_active is True)

    def test_default(self):
        user = User(username='haha', email='haha@haha.com', password='345')
        user.save()

        self.assertTrue(user.is_active is False)
        self.assertTrue(user.is_admin is False)
        self.assertTrue(isinstance(user.create_at, datetime.datetime) is True)








