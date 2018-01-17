from app.exetensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask import current_app

Column = db.Column


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(80), nullable=False, unique=True)
    password_hash = Column(db.String(128))
    email = Column(db.String(50), unique=True)
    create_at = Column(db.DateTime, default=datetime.now())
    active = Column(db.Boolean, default=False)
    is_admin = Column(db.Boolean, default=False)

    def __init__(self, username, email, password, active=False, is_admin=False, create_at=datetime.now()):
        self.username = username
        self.email = email
        self.active = active
        self.is_admin = is_admin
        self.create_at = create_at
        if password:
            self.password_hash = generate_password_hash(password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})


    @classmethod
    def confirm(cls, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        user = cls.query.filter_by(id=data.get('confirm', '')).first()
        return user

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not readable!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<user: {}>'.format(self.username)


class Snptable(db.Model):
    id = Column(db.Integer, primary_key=True)
    tablename = Column(db.String(45))
    tabletype = Column(db.String(45))
    owner = Column(db.String(80))

    def __repr__(self):
        return '<snp table {}>'.format(self.id)








