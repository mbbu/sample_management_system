import os

from api.constants import APP_NAME, DATABASE_URI_ENV_NAME


class BaseConfig(object):
    database_uri = os.getenv(DATABASE_URI_ENV_NAME)
    SQLALCHEMY_DATABASE_URI = database_uri
    SECRET_KEY = os.environ.get(APP_NAME + "_SECRET_KEY")


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ENV = "development"
    DEBUG = True


class ProductionConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "production"
    DEBUG = False
