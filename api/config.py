import os

from api.constants import APP_NAME, DATABASE_URI_ENV_NAME


class BaseConfig(object):
    database_uri = os.getenv(DATABASE_URI_ENV_NAME)
    SQLALCHEMY_DATABASE_URI = database_uri
    SECRET_KEY = os.environ.get(APP_NAME + "_SECRET_KEY")

    # ADMIN MAILING CONFIG
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['jeffkim207@gmail.com']


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ENV = "development"
    DEBUG = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "production"
    DEBUG = False
