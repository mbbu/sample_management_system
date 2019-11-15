import logging
from logging.handlers import RotatingFileHandler

import os

from flask import Flask
from flask_restful import Api
from flask_login import LoginManager

from api.constants import APP_CONFIG_ENV_VAR, DEV_CONFIG_VAR, PROD_CONFIG_VAR, APP_NAME
from api.models.database import BaseModel


def get_config_type():
    return os.environ.get(APP_CONFIG_ENV_VAR, PROD_CONFIG_VAR).lower().strip()


def file_logging(app_instance):
    if not os.path.exists('logs'):
        os.mkdir('logs')

    handler = RotatingFileHandler('logs/' + APP_NAME + ".log")
    handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s]: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    handler.setLevel(logging.DEBUG)

    app_instance.logger.addHandler(handler)
    app_instance.logger.setLevel(logging.DEBUG)
    app_instance.logger.info(APP_NAME)


# noinspection PyTypeChecker
def register_resources(app):
    # TODO: import resources here
    from api.resources.hello_world_resource import HelloWorldResource

    api = Api(app)
    api.add_resource(HelloWorldResource, '/welcome')
    # TODO: register resources here


def config_app(app_instance):
    config_type = get_config_type()
    file_logging(app_instance)

    # possible configurations as a dictionary
    configs = {
        DEV_CONFIG_VAR: "api.config.DevelopmentConfig",
        PROD_CONFIG_VAR: "api.config.ProductionConfig"
    }

    app_instance.config.from_object(configs[config_type])
    config_file_path = os.environ.get(APP_NAME + "_CONFIG_FILE")

    if config_file_path and os.path.exists(config_file_path):
        app_instance.config.from_pyfile(config_file_path)

    # Ensure flask doesn't redirect to trailing slash endpoint
    app_instance.url_map.strict_slashes = False


login = LoginManager()


# Application Factory
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        app.config.from_mapping(test_config)
    else:
        config_app(app)

    # Ensure instance path exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register Resources
    register_resources(app)

    #  LoginManager
    login.init_app(app)
    login.login_view = 'login_bp.login'

    # Database and Migrations setup
    db = BaseModel.init_app(app)

    @app.shell_context_processor
    def make_shell_processor():
        return {
            'db': BaseModel.init_db(app),
            'models': BaseModel.migrate_db(app, db)
        }

    @app.route('/')
    def index():
        app.logger.info('Welcome Page Accessed!By {0}')
        return 'Hello, Welcome to MBBU Sample Management System!'

    return app


@login.user_loader
def load_user(user_id):
    from api.models.user import User
    BaseModel.db.session.query(User).get(int(user_id))
