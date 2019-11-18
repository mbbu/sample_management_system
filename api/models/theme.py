from api.models.database import BaseModel


class Theme(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    name = AppDb.Column(AppDb.String(65), nullable=False, index=True)

    # relationship
    sample = AppDb.relationship('Sample', backref='theme', lazy=True)
