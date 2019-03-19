import os


class BaseConfig:
    PROJECT = 'Poebot'
    DEBUG = True
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    SECRET_KEY = os.urandom(32)

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_FILE = '{}.sqlite'.format(PROJECT)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'Poebot-web', DATABASE_FILE)
