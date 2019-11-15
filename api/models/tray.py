from api.models.database import BaseModel


class Tray(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    rack_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('rack.id'))
    number = AppDb.Column(AppDb.Integer, nullable=False)  # todo: should be unique?

    # relationship(s)
    rack = AppDb.relationship('Rack', backref='tray', lazy=True)

    def __repr__(self):
        return '<< Tray: (number={0} || rack={1}) >>'.format(self.number, self.rack_id)
