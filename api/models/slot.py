from sqlalchemy.orm import backref

from api.models.database import BaseModel
from api.search.searchable_mixin import SearchableMixin


class Slot(BaseModel.db.Model, SearchableMixin):
    __tablename__ = index_name = 'slot'
    __searchable__ = ['code', 'position', 'available']

    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    box_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('box.id', ondelete='CASCADE'), nullable=False)
    code = AppDb.Column(AppDb.String(65), nullable=False, unique=True, index=True)
    position = AppDb.Column(AppDb.JSON, nullable=True)
    available = AppDb.Column(AppDb.Boolean, nullable=False, default=True)

    # relationships
    box = AppDb.relationship('Box', backref=backref('slots', cascade='all, delete-orphan'))

    __mapper_args__ = {
        "order_by": id
    }

    def __init__(self, box, code, pos):
        self.box_id = box
        self.code = code
        self.pos = pos

    def __repr__(self):
        return '<< Slot: (box={0} || pos={1} || available={2}) >>'.format(self.box, self.position, self.available)

    @staticmethod
    def slot_exists(code):
        if Slot.query.filter(
                Slot.code == code
        ).first():
            return True
        return False
