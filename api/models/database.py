from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


class BaseModel(object):
    db = None

    @staticmethod
    def init_db(app):
        BaseModel.db = SQLAlchemy(app)
        return BaseModel.db

    @staticmethod
    def migrate_db(app, db):
        # ToDo imports of models to be placed here
        from api.models.role import Role
        from api.models.user import User
        from api.models.sample import Sample
        from api.models.box import Box
        from api.models.tray import Tray
        from api.models.rack import Rack
        from api.models.chamber import Chamber
        from api.models.freezer import Freezer
        from api.models.laboratory import Laboratory
        from api.models.publication import  Publication
        Migrate(app, db)

    @staticmethod
    def init_app(app):
        BaseModel.init_db(app)
        BaseModel.migrate_db(app, BaseModel.init_db(app))
