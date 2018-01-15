# coding=utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'djaildhjsdfhjs'
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USER')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWD')
    MAIL_SUBJECT_PREFIX = '[SNP INDEX]'
    MAIL_SENDER = 'Snp Index Admin <{0}>'.format(MAIL_USERNAME)
    # Celery
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_MAP = {'qq': '',
                '163': ''}

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    ENV = 'dev'
    DB_NAME = 'dev.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, DB_NAME)
    Debug = True


class TestConfig(Config):
    ENV = 'test'
    DB_NAME = 'test.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, DB_NAME)
    DEBUG = True


class ProdConfig(Config):
    ENV = 'prod'
    SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{passwd}@{host}/{db}'.format(
        user=os.environ['DB_USER'],
        passwd=os.environ['DB_PASSWD'],
        host='localhost',
        db='snp_index'
    )
    DEBUG = False


config = {'default': DevConfig,
          'test': TestConfig,
          'prod': ProdConfig,
          'dev': DevConfig}


