from api.models.database import BaseModel
from api.search.searchable_mixin import SearchableMixin


class Freezer(BaseModel.db.Model, SearchableMixin):
    __tablename__ = index_name = 'freezer'
    __searchable__ = ['code', 'room', 'number']

    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    laboratory_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('laboratory.id', ondelete='SET NULL'), nullable=True)
    number = AppDb.Column(AppDb.Integer, nullable=False)
    room = AppDb.Column(AppDb.String(65), nullable=False)
    code = AppDb.Column(AppDb.String(65), nullable=False)

    # relationship(s)
    lab = AppDb.relationship('Laboratory', backref='freezer', lazy=True)

    @staticmethod
    def freezer_exists(code):
        if Freezer.query.filter(
                Freezer.code == code
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< Freezer: (number={0} || room={1} || lab={2} || code={3}) >>' \
            .format(self.number, self.room, self.laboratory_id, self.code)
