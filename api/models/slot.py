from sqlalchemy.orm import backref

from api.models.database import BaseModel


class Slot(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    box_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('box.id'), nullable=False)
    code = AppDb.Column(AppDb.String(65), nullable=False, unique=True, index=True)
    position = AppDb.Column(AppDb.JSON, nullable=True)
    available = AppDb.Column(AppDb.Boolean, nullable=False, default=True)

    # relationships
    box = AppDb.relationship('Box', backref=backref('slots', cascade='all, delete-orphan'))

    @staticmethod
    def slot_exists(code):
        if Slot.query.filter(
                Slot.code == code
        ).first():
            return True
        return False
