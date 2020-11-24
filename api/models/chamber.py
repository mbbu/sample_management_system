from api.models.database import BaseModel
from api.search.searchable_mixin import SearchableMixin


class Chamber(BaseModel.db.Model, SearchableMixin):
    __tablename__ = index_name = 'chamber'
    __searchable__ = ['code', 'type']

    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    freezer_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('freezer.id', ondelete='SET NULL'), nullable=True)
    type = AppDb.Column(AppDb.String(50), nullable=False)
    code = AppDb.Column(AppDb.String(65), nullable=False)

    # relationship(s)
    freezer = AppDb.relationship('Freezer', backref='chamber', lazy=True)

    @staticmethod
    def chamber_exists(code):
        if Chamber.query.filter(
            Chamber.code == code
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< Chamber:  (type={0} || freezer={1} || code={2}) >>'.format(self.type, self.freezer_id, self.code)
