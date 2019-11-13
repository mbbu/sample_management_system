from api.models.database import BaseModel

class Freezer(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key= True)
    laboratory_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('laboratory.id'))
    freezer_number = AppDb.Column(AppDb.Integer, nullable = False)
    room_located = AppDb.Column(AppDb.String(65), nullable = False)

    # todo: relationships defined here
    chamberinfreezer = AppDb.relationship('Chamber', backref='chamber_position', lazy= 'dynamic')

    def __repr__(self):
        return '<Freezer {}>'.format(self.laboratory_id, self.freezer_number, self.room_located)
