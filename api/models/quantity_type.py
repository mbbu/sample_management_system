from api.models.database import BaseModel
from api.search.searchable_mixin import SearchableMixin


class QuantityType(BaseModel.db.Model, SearchableMixin):
    __tablename__ = index_name = 'quantity_type'
    __searchable__ = ['id', 'name', 'description']

    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.String(5), primary_key=True)
    name = AppDb.Column(AppDb.String(30), nullable=False)
    description = AppDb.Column(AppDb.String(255), nullable=True)

    @staticmethod
    def exists(_id):
        if QuantityType.query.filter(
                QuantityType.id == _id
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< QuantityType: (id={0} || name={1}) >>'.format(self.id, self.name)
