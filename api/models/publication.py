from api.models.database import BaseModel


class Publication(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    sample_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('sample.id'))
    user_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('users.id'))
    sample_results = AppDb.Column(AppDb.String(150), nullable=False)
    title = AppDb.Column(AppDb.String(150), nullable=True)
    co_authors = AppDb.Column(AppDb.String(150), nullable=True)

    # todo: relationships defined here
    userhaspublication = AppDb.relationship('User', backref='publication', lazy='dynamic')

    def __repr__(self):
        return '<Publication {}>'.format(self.sample_id, self.user_id, self.sample_results, self.title,
                                         self.co_authors)
