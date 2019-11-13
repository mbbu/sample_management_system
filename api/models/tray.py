from api.models.database import BaseModel


class Tray(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key = True)
    rack_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('rack.id'))
    tray_number = AppDb.Column(AppDb.Integer, nullable = False)

    # todo: relationships defined here
    boxintray = AppDb.relationship('Box', backref='tray_position', lazy= 'dynamic')

def __repr__(self):
    return '<Tray {}>'.format(self.rack_id, self.tray_number)