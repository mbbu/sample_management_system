from api.models.database import BaseModel


class Rack(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    chamber_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('chamber.id'))
    number = AppDb.Column(AppDb.Integer, nullable=False)

    # relationships
    chamber = AppDb.relationship('Chamber', backref='rack', lazy=True)
    #tray= AppDb.relationship('Tray', backref='rack', lazy=True)

    def __repr__(self):
        return '<< Rack: (number={0} || chamber={1} ) >>'.format(self.number, self.chamber_id)
