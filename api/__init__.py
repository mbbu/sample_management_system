import logging
import logging.handlers
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_restful import Api

from api.constants import APP_CONFIG_ENV_VAR, DEV_CONFIG_VAR, PROD_CONFIG_VAR, APP_NAME


def get_config_type():
    return os.environ.get(APP_CONFIG_ENV_VAR, PROD_CONFIG_VAR).lower().strip()


def file_logging(app_instance):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    app_instance.logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler('logs/' + APP_NAME + ".log")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s [in %(pathname)s:%(lineno)d]'))

    app_instance.logger.addHandler(handler)


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

    register_resources(app)

    @app.route('/')
    def index():
        return 'Hello, Welcome to MBBU Sample Management System!'

    return app
