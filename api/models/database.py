from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


class BaseModel(object):
    db = SQLAlchemy()

    @staticmethod
    def init_db(app):
        BaseModel.db = SQLAlchemy(app)
        return BaseModel.db

    @staticmethod
    def migrate_db():
        # ToDo imports of models to be placed here
        from api.models.role import Role
        from api.models.sample import Sample
        from api.models.theme import Theme
        from api.models.user import User
        from api.models.box import Box
        from api.models.tray import Tray
        from api.models.rack import Rack
        from api.models.chamber import Chamber
        from api.models.freezer import Freezer
        from api.models.laboratory import Laboratory
        from api.models.publication import Publication
        from api.models.quantity_type import QuantityType
        from api.models.project import Project
        from api.models.sample_request import SampleRequest
        return [
            Role, User, Theme, Sample,
            Box, Tray, Rack, QuantityType, Chamber,
            Freezer, Laboratory, Publication, Project, SampleRequest
        ]

    @staticmethod
    def init_app(app):
        db = BaseModel.init_db(app)
        Migrate(app=app, db=db, compare_type=True)
