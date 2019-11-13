from api.models.database import BaseModel

class Laboratory (BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key = True)
    lab_name = AppDb.Column(AppDb.String(65), nullable = False)
    room_number = AppDb.Column(AppDb.Integer)

     # todo: relationships defined here
    freezerinlab = AppDb.relationship('Freezer', backref='freezer_position', lazy= 'dynamic')

    def __repr__(self):
        return '<Laboratory {}>'.format(self.lab_name, self.room_number)