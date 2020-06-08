from datetime import datetime

from api.models.database import BaseModel


class SampleRequest(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    user = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('users.id', ondelete='SET NULL'), nullable=False)
    sample = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('sample.id', ondelete='SET NULL'), nullable=False)
    amount = AppDb.Column(AppDb.Integer, nullable=False)  # amount being requested
    request_date = AppDb.Column(AppDb.DateTime, nullable=False, default=datetime.now)
    response_date = AppDb.Column(AppDb.DateTime, nullable=True)
    status = AppDb.Column(AppDb.String(25), nullable=False)  # is the request pending, approved or rejected?
    notes = AppDb.Column(AppDb.Text, nullable=True)  # Any special issues about the sample request e.g. on reject
