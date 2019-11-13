from api.models.database import BaseModel


class Rack(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key = True)
    chamber_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('chamber.id'))
    rack_number = AppDb.Column(AppDb.Integer, nullable = False)

    # todo: relationships defined here
    rackintray = AppDb.relationship('Tray', backref='rack_position', lazy= 'dynamic')

def __repr__(self):
    return '<Rack {}>'.format( self.chamber_id ,self.rack_number)