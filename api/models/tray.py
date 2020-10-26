from api.models.database import BaseModel
from api.search.searchable_mixin import SearchableMixin


class Tray(BaseModel.db.Model, SearchableMixin):
    __tablename__ = index_name = 'tray'
    __searchable__ = ['code', 'number']

    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    rack_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('rack.id', ondelete='SET NULL'), nullable=True)
    number = AppDb.Column(AppDb.Integer, unique=True, nullable=False)
    code = AppDb.Column(AppDb.String, nullable=False)

    # relationship(s)
    rack = AppDb.relationship('Rack', backref='tray', lazy=True)

    @staticmethod
    def tray_exists(code):
        if Tray.query.filter(
            Tray.code == code
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< Tray: (number={0} || rack={1} || code={2}) >>'.format(self.number, self.rack_id, self.code)
