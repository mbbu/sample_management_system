from api.models.database import BaseModel


class Tray(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    rack_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('rack.id'))
    number = AppDb.Column(AppDb.Integer, nullable=False)

    # relationships
    boxintray = AppDb.relationship('Box', backref='tray', lazy='dynamic')

    def __repr__(self):
        return '<Tray {}>'.format(self.rack_id, self.number)
