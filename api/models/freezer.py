from api.models.database import BaseModel
from api.search.searchable_mixin import SearchableMixin


class Freezer(BaseModel.db.Model, SearchableMixin):
    __tablename__ = index_name = 'freezer'
    __searchable__ = ['code', 'number']

    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    laboratory_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('laboratory.id', ondelete='SET NULL'), nullable=True)
    number = AppDb.Column(AppDb.Integer, nullable=False)
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

    def __init__(self, lab, num, code):
        self.laboratory_id = lab
        self.number = num
        self.code = code

    def __repr__(self):
        return '<< Freezer: (number={0} || lab={1} || code={2}) >>' \
            .format(self.number, self.laboratory_id, self.code)
