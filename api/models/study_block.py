from api.models.database import BaseModel
from api.search.searchable_mixin import SearchableMixin


class StudyBlock(BaseModel.db.Model, SearchableMixin):
    __tablename__ = index_name = 'study_block'
    __searchable__ = ['code', 'name']

    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    area = AppDb.Column(AppDb.String(65), nullable=True, unique=False)
    code = AppDb.Column(AppDb.String(10), nullable=False, unique=True, index=True)
    name = AppDb.Column(AppDb.String(65), nullable=False, unique=True, index=True)

    # relationship
    house_hold_data = AppDb.relationship('AnimalHealthHouseData', backref='study_block', lazy=True)
    samples = AppDb.relationship('Sample', backref='study_block', lazy=True)

    @staticmethod
    def study_block_exists(code):
        if StudyBlock.query.filter(
                StudyBlock.code == code
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< StudyBlock: (area={0} || code={1} || name={2}) >>'.format(self.area, self.code, self.name)
