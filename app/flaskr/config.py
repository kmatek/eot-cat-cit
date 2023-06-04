import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('DEBUG')
    HOST = os.environ.get('HOST')
    PORT = os.environ.get('PORT')


class TestingConfig(Config):
    TESTING = True
