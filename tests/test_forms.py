import unittest
from app.auth.forms import LoginForm, RegisterForm
from app.auth.models import User
from app.exetensions import db
from app.app import create_app


class LoginFormCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_active(self):
        user = User(username='cc', email='cc@qq.com', password='123')
        user.save()

        form = LoginForm(username=user.username, password='123')
        self.assertTrue(form.validate() is False)

    def test_user_login(self):
        user = User(username='cc', email='cc@qq.com', password='123', is_active=True)
        user.save()

        form = LoginForm(username=user.username, password='123')
        self.assertTrue(form.validate() is True)


class RegisterFormTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_password(self):
        form = RegisterForm(username='js', email='js@qq.com', password='123', confirm='321')
        self.assertFalse(form.validate() is True)

    def test_user_exist(self):
        user = User(username='cc', email='cc@qq.com', password='123')
        user.save()

        form = RegisterForm(username='cc', email='js@qq.com', password='123', confirm='123')
        self.assertFalse(form.validate() is True)

    def test_email_exist(self):
        user = User(username='cc', email='cc@qq.com', password='123')
        user.save()

        form = RegisterForm(username='js', email='cc@qq.com', password='123', confirm='123')
        self.assertFalse(form.validate() is True)

    def test_register(self):
        form = RegisterForm(username='js', email='js@qq.com', password='123', confirm='123')
        self.assertTrue(form.validate() is True)











