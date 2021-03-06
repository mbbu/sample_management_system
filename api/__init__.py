import logging
import os
from logging.handlers import RotatingFileHandler
from logging.handlers import SMTPHandler

from elasticsearch import Elasticsearch
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound, InternalServerError

from api.config import BaseConfig
from api.constants import APP_CONFIG_ENV_VAR, DEV_CONFIG_VAR, PROD_CONFIG_VAR, APP_NAME, SECRET_KEY, revoked_store
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
    from .resources.index_resource import IndexResource
    from .resources.auth_resource import AuthResource, LogOutResource
    from .resources.theme_resource import ThemeResource
    from .resources.study_block_resource import StudyBlockResource
    from .resources.sample_resource import SampleResource
    from .resources.user_resource import UserResource
    from .resources.publication_resource import PublicationResource
    from .resources.box_resource import BoxResource
    from .resources.role_resource import RoleResource
    from .resources.tray_resource import TrayResource
    from .resources.rack_resource import RackResource
    from .resources.chamber_resource import ChamberResource
    from .resources.freezer_resource import FreezerResource
    from .resources.lab_resource import LaboratoryResource
    from .resources.quantity_type_resource import QuantityTypeResource
    from .resources.bio_hazard_level_resource import BioHazardLevelResource
    from .resources.housedata_resource import HouseDataResource
    from .resources.email_confirmation.email_confirmation import EmailConfirmationResource
    from .resources.project_resource import ProjectResource
    from .resources.redcap_requests.fetch_sample_resource import SaveSampleFromREDCap
    from .resources.sample_request_and_response.sample_request_resource import SampleRequestResource
    from .resources.sample_request_and_response.sample_request_response import SampleRequestResponseResource
    from .resources.password_reset.password_reset import ForgotPasswordResource, PasswordResetResource
    from .resources.slot_resource import SlotResource

    api = Api(app)
    api.add_resource(IndexResource, '/', '/index', '/welcome')
    api.add_resource(AuthResource, '/auth', '/login', '/auth/login')
    api.add_resource(LogOutResource, '/logout', '/log-out')
    api.add_resource(ThemeResource, '/theme', '/themes')
    api.add_resource(StudyBlockResource, '/study-block', '/study_block')
    api.add_resource(ProjectResource, '/project', '/projects')
    api.add_resource(RoleResource, '/role', '/roles')
    api.add_resource(UserResource, '/user', '/users')

    api.add_resource(EmailConfirmationResource, '/requestConfirmation', '/confirm/<token>')
    api.add_resource(ForgotPasswordResource, '/forgot')
    api.add_resource(PasswordResetResource, '/reset/<token>')

    api.add_resource(PublicationResource, '/publication', '/publications')
    api.add_resource(SampleResource, '/sample', '/samples')
    api.add_resource(SampleRequestResource, '/sample-request', '/request-sample')
    api.add_resource(SampleRequestResponseResource, '/sample-request-response/<token>', '/request-response/<token>')
    api.add_resource(SaveSampleFromREDCap, '/redcap-samples')
    api.add_resource(BoxResource, '/box', '/boxes')
    api.add_resource(SlotResource, '/slots/<box>/<row>/<col>', '/slot')
    api.add_resource(TrayResource, '/tray', '/trays')
    api.add_resource(RackResource, '/rack', '/racks')

    api.add_resource(ChamberResource, '/chamber', '/chambers')
    api.add_resource(FreezerResource, '/freezer', '/freezers')
    api.add_resource(LaboratoryResource, '/lab', '/laboratory')

    api.add_resource(QuantityTypeResource, '/quantity-type')
    api.add_resource(BioHazardLevelResource, '/bio-hazard-level')

    api.add_resource(HouseDataResource, '/house-data')

    from api.resources.faker_resource import FakeDataResource
    api.add_resource(FakeDataResource, '/faker')

    # Error handlers
    # api.handle_error(500)
    # api.error_router()


def config_app(app_instance):
    config_type = get_config_type()
    file_logging(app_instance)
    mail_admin(app_instance)

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


db = SQLAlchemy()


def extensions_set_up(app_instance):
    app_instance.config['SECRET_KEY'] = os.getenv(SECRET_KEY)
    # JWT setup
    jwt = JWTManager(app_instance)

    # Flask-Mail SetUp
    mail = Mail(app_instance)

    # Database and Migrations setup
    db.init_app(app_instance)
    migrate = Migrate(app_instance, db, compare_type=True)

    return {'jwt': jwt, 'mail': mail, 'db': db, 'migrate': migrate}


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

    # Cross-Origin Resource Sharing
    CORS(app, resources={r"/*": BaseConfig.cors_config})

    # Extensions SetUp
    ext = extensions_set_up(app)
    jwt = ext.get('jwt')

    app.elasticsearch = Elasticsearch([BaseConfig.ELASTICSEARCH_URL]) \
        if BaseConfig.ELASTICSEARCH_URL else None

    @jwt.token_in_blacklist_loader
    def check_if_token_is_revoked(decrypted_token):
        jti = decrypted_token['jti']
        entry = revoked_store.get(jti)
        if entry is None:
            return True
        return entry == 'true'

    @app.shell_context_processor
    def make_shell_processor():
        return {
            'db': db,
        }

    @app.route('/home')
    def home():
        return 'Hello, Welcome to M.B.B.U Sample Management System!'

    @app.errorhandler(NotFound)
    def not_found_error(error):
        app.logger.info(error)
        return BaseResource.send_json_message('Sorry we couldn\'t find what you were looking for.', 404)

    @app.errorhandler(InternalServerError)
    def internal_error(error):
        db.session.rollback()
        app.logger.error(error)
        return BaseResource.send_json_message('An unexpected error occurred!'
                                              'But stay put the administrator has been notified.'
                                              'Sorry for the inconvenience!', 500)

    return app
