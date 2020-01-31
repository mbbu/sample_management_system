import logging
import os

from flask import has_request_context, request

from api.constants import DATABASE_URI_ENV_NAME, SECRET_KEY, ACCESS_EXPIRES, REFRESH_EXPIRES


# override default log formats
class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None
        return super().format(record)


class BaseConfig(object):
    database_uri = os.getenv(DATABASE_URI_ENV_NAME)
    SQLALCHEMY_DATABASE_URI = database_uri
    SECRET_KEY = os.environ.get(SECRET_KEY) or os.urandom(32)

    # ADMIN MAILING CONFIG
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['cynthiakamau54@gmail.com']

    # Add Custom log format to config
    LOGGING_FORMAT = RequestFormatter(
        '[%(asctime)s] Remote Address:%(remote_addr)s requested %(url)s\n'
        ' [%(levelname)s]: %(message)s [in %(pathname)s::%(lineno)d]\n'
    )

    # Redis
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    PROPAGATE_EXCEPTIONS = True

    # REDCap API Token
    REDCap_API_TOKEN = os.environ.get('REDCap_API_TOKEN')


class TestConfig(BaseConfig):
    configs = {"TESTING": True,
               'SQLALCHEMY_DATABASE_URI': BaseConfig.SQLALCHEMY_DATABASE_URI,
               'SQLALCHEMY_TRACK_MODIFICATIONS': False}


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ENV = "development"
    DEBUG = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "production"
    DEBUG = False
