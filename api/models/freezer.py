from api.models.database import BaseModel


class Freezer(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    laboratory_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('laboratory.id'))
    freezer = AppDb.Column(AppDb.Integer, nullable=False)  # todo change freezer to number
    room = AppDb.Column(AppDb.String(65), nullable=False)

    # todo: relationships defined here
    chamberinfreezer = AppDb.relationship('Chamber', backref='freezer', lazy='dynamic')

    def __repr__(self):
        return '<Freezer {}>'.format(self.laboratory_id, self.freezer, self.room)
