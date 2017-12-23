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
    MAIL_SUBJECT_PREFIX = ['SNP INDEX']
    MAIL_SENDER = 'Snp Index Admin <0>'.format(MAIL_USERNAME)

    @staticmethod
    def init_app(app):
        pass


config = {'default': Config}
