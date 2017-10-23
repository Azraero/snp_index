# coding=utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'djaildhjsdfhjs'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    HOSTBNAME = 'localhost'
    DATABASE = 'snp_index'
    DEBUG = True
    DB_USERNAME = os.environ.get('USERNAME', 'root')
    DB_PASSWORD = os.environ.get('PASSWORD', '050400')
    DB_URI = 'mysql://{}:{}@{}/{}'.format(
        DB_USERNAME,
        DB_PASSWORD,
        HOSTBNAME,
        DATABASE)


class ProductionConfig(Config):
        HOSTBNAME = 'localhost'
        DATABASE = 'snp_index'
        DB_USERNAME = os.environ.get('USERNAME', 'onmaisiadmin')
        DB_PASSWORD = os.environ.get('PASSWORD', 'onmaisiadmin')
        DB_URI = 'mysql://{}:{}@{}/{}'.format(
            DB_USERNAME,
            DB_PASSWORD,
            HOSTBNAME,
            DATABASE)


config = {'develop': DevelopmentConfig,
          'product': ProductionConfig,
          'default': DevelopmentConfig}
