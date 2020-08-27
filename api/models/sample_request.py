from datetime import datetime

from api.models.database import BaseModel


class SampleRequest(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    user = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('users.id', ondelete='SET NULL'),
                        nullable=False)
    sample = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('sample.id', ondelete='SET NULL'), nullable=False)
    amount = AppDb.Column(AppDb.Integer, nullable=False)  # amount being requested
    request_date = AppDb.Column(AppDb.DateTime, nullable=False, default=datetime.now)
    response_date = AppDb.Column(AppDb.DateTime, nullable=True)
    status = AppDb.Column(AppDb.String(25), nullable=False)  # is the request pending, approved or rejected?
    notes = AppDb.Column(AppDb.Text, nullable=True)  # Any special issues about the sample request e.g. on reject
    approved_amount = AppDb.Column(AppDb.Integer, nullable=True, default=0)

    def __repr__(self):
        return '<< SampleRequest: (user={0} || sample={1} || amount={2} ' \
               '|| request_date={3} || response_date={4}) || status={5} || notes={6}>>'\
            .format(self.user, self.sample, self.amount, self.request_date, self.response_date, self.status, self.notes)
