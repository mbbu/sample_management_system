from api.models.database import BaseModel


class Role(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    code = AppDb.Column(AppDb.String(20), nullable=False, unique=True, index=True)
    name = AppDb.Column(AppDb.String(50), nullable=False)
    description = AppDb.Column(AppDb.String(255), nullable=True)

    # todo: relationships defined here
    user = AppDb.relationship('User', backref='role', lazy='dynamic')
