from api.models.database import BaseModel


class Rack(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    chamber_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('chamber.id'))
    number = AppDb.Column(AppDb.Integer, nullable=False)

    # relationships
    rackintray = AppDb.relationship('Tray', backref='rack', lazy='dynamic')

    def __repr__(self):
        return '<Rack {}>'.format(self.chamber_id, self.number)
