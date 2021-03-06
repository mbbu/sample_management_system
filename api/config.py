import logging
import os

from flask import has_request_context, request

from api.constants import DATABASE_URI_ENV_NAME, SECRET_KEY, ACCESS_EXPIRES, REFRESH_EXPIRES, SECURITY_PASSWORD_SALT


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
    SECURITY_PASSWORD_SALT = os.environ.get(SECURITY_PASSWORD_SALT) or os.urandom(32)
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    # ADMIN MAILING CONFIG
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('MAIL_USERNAME')

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

    # CORS
    cors_config = {
       "origins": ["http://localhost", "http://localhost:80",
                   "http://localhost:8080", "http://lims.icipe.org:8080",
                   "http://lims.icipe.org", "http://lims.icipe.org:80"],
       "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
       "allow_headers": ["Authorization", "Content-Type", "code", "title", "email"]
    }


class TestConfig(BaseConfig):
    configs = {"TESTING": True,
               'SQLALCHEMY_DATABASE_URI': 'sqlite:////',
               'SQLALCHEMY_TRACK_MODIFICATIONS': False}


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ENV = "development"
    DEBUG = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "production"
    DEBUG = False
