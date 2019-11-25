from api.models.database import BaseModel


class Rack(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    chamber_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('chamber.id'))
    number = AppDb.Column(AppDb.Integer, nullable=False)  # todo: is this unique?
    code = AppDb.Column(AppDb.String(65), nullable=False)

    # relationships
    chamber = AppDb.relationship('Chamber', backref='rack', lazy=True)

    @staticmethod
    def rack_exists(num):
        if Rack.query.filter(
                Rack.number == num
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< Rack: (number={0} || chamber={1} || code={3}) >>'.format(self.number, self.chamber_id, self.code)
