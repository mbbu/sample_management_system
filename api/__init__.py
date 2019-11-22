import logging
import os
from logging.handlers import RotatingFileHandler
from logging.handlers import SMTPHandler

from flask import Flask
from flask_login import LoginManager
from flask_restful import Api

from api.config import BaseConfig
from api.constants import APP_CONFIG_ENV_VAR, DEV_CONFIG_VAR, PROD_CONFIG_VAR, APP_NAME
from api.models.database import BaseModel
from api.resources.base_resource import BaseResource


def get_config_type():
    return os.environ.get(APP_CONFIG_ENV_VAR, PROD_CONFIG_VAR).lower().strip()


def file_logging(app_instance):
    if not os.path.exists('logs'):
        os.mkdir('logs')

    handler = RotatingFileHandler('logs/' + APP_NAME + ".log")
    handler.setFormatter(BaseConfig.LOGGING_FORMAT)
    handler.setLevel(logging.DEBUG)

    app_instance.logger.addHandler(handler)
    app_instance.logger.setLevel(logging.DEBUG)
    app_instance.logger.info(APP_NAME)


def mail_admin(app):
    if BaseConfig.MAIL_SERVER:
        auth = None
        if BaseConfig.MAIL_USERNAME or BaseConfig.MAIL_PASSWORD:
            auth = (BaseConfig.MAIL_USERNAME, BaseConfig.MAIL_PASSWORD)

        secure = None
        if BaseConfig.MAIL_USE_TLS:
            secure = ()

        mail_handler = SMTPHandler(
            mailhost=(BaseConfig.MAIL_SERVER, BaseConfig.MAIL_PORT),
            fromaddr='no-reply@' + BaseConfig.MAIL_SERVER,
            toaddrs=BaseConfig.ADMINS,
            subject='Sample Management System Failure',
            credentials=auth,
            secure=secure
        )

        mail_handler.setFormatter(BaseConfig.LOGGING_FORMAT)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    pass


# noinspection PyTypeChecker
def register_resources(app):
    # TODO: import resources here
    from api.resources.hello_world_resource import HelloWorldResource
    from api.resources.theme_resource import ThemeResource
    from api.resources.sample_resource import SampleResource
    from api.resources.user_resource import UserResource
    from api.resources.publication_resource import PublicationResource
    from api.resources.box_resource import BoxResource
    from api.resources.role_resource import RoleResource
    from api.resources.tray_resource import TrayResource
    from api.resources.rack_resource import RackResource
    from api.resources.chamber_resource import ChamberResource
    from api.resources.freezer_resource import FreezerResource

    api = Api(app)
    api.add_resource(HelloWorldResource, '/', '/index', '/welcome')
    api.add_resource(SampleResource, '/sample', '/samples', '/sample/<id>')
    api.add_resource(ThemeResource, '/theme', '/themes', '/theme/<id>')
    api.add_resource(UserResource, '/user', '/users', '/user/<email>')
    api.add_resource(PublicationResource, '/publication', '/publications', '/publication/<id>')
    api.add_resource(BoxResource, '/box','/boxes', '/box/<label>')
    api.add_resource(RoleResource, '/role', '/roles', '/role/<code>')
    api.add_resource(TrayResource, '/tray', '/trays', '/tray/<num>')
    api.add_resource(RackResource, '/rack', '/racks', '/rack/<num>')
    api.add_resource(ChamberResource, '/chamber', '/chambers', '/chamber/<c_type>')
    api.add_resource(FreezerResource, '/freezer', '/freezers', '/freezer/<number>')

    # TODO: register resources here


def config_app(app_instance):
    config_type = get_config_type()
    file_logging(app_instance)
    # mail_admin(app_instance) todo: uncomment when app is in production

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
            'models': BaseModel.migrate_db()
        }

    @app.route('/')
    def index():
        from flask_login import current_user
        app.logger.info('Welcome Page Accessed!By {0}'.format(current_user))
        return 'Hello, Welcome to MBBU Sample Management System!'

    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.info(error)
        return BaseResource.send_json_message('Sorry we couldn\'t find what you were looking for.', 404)

    @app.errorhandler(500)
    def internal_error(error):
        BaseModel.init_db(app).session.rollback()
        app.logger.error(error)
        return BaseResource.send_json_message('An unexpected error occurred!'
                                              ' But stay put the administrator has been notified. '
                                              'Sorry for the inconvenience!', 500)

    return app


@login.user_loader
def load_user(user_id):
    from api.models.user import User
    BaseModel.db.session.query(User).get(int(user_id))
