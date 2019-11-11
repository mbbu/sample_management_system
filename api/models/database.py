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
        Migrate(app, db)

    @staticmethod
    def init_app(app):
        BaseModel.init_db(app)
        BaseModel.migrate_db(app, BaseModel.init_db(app))
