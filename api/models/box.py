from api.models.database import BaseModel
from api.search.searchable_mixin import SearchableMixin


class Box(BaseModel.db.Model, SearchableMixin):
    __tablename__ = index_name = 'box'
    __searchable__ = ['code', 'label']

    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    tray_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('tray.id', ondelete='SET NULL'), nullable=True)
    label = AppDb.Column(AppDb.String(65), nullable=False)
    code = AppDb.Column(AppDb.String(65), nullable=False, unique=True, index=True)

    # relationship(s)
    tray = AppDb.relationship('Tray', backref='box', lazy=True)

    def __init__(self, tray, label, code):
        self.tray_id = tray
        self.label = label
        self.code = code

    def __repr__(self):
        return '<< Box: (label={0} || tray={1} || code={2}) >>'.format(self.label, self.tray_id, self.code)

    @staticmethod
    def box_exists(code):
        if Box.query.filter(
                Box.code == code
        ).first():
            return True
        return False
