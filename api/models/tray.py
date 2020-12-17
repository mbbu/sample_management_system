from api.models.database import BaseModel
from api.search.searchable_mixin import SearchableMixin


class Tray(BaseModel.db.Model, SearchableMixin):
    __tablename__ = index_name = 'tray'
    __searchable__ = ['code', 'number']

    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    rack_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('rack.id', ondelete='CASCADE'), nullable=True)
    number = AppDb.Column(AppDb.Integer, nullable=False)
    code = AppDb.Column(AppDb.String, unique=True, nullable=False)

    # relationship(s)
    rack = AppDb.relationship('Rack', backref='tray', lazy=True)

    __mapper_args__ = {
        "order_by": id
    }

    @staticmethod
    def tray_exists(code):
        if Tray.query.filter(
            Tray.code == code
        ).first():
            return True
        return False

    def __init__(self, rack, num, code):
        self.rack_id = rack
        self.number = num
        self.code = code

    def __repr__(self):
        return '<< Tray: (number={0} || rack={1} || code={2}) >>'.format(self.number, self.rack_id, self.code)
