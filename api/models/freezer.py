from api.models.database import BaseModel


class Freezer(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    laboratory_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('laboratory.id', ondelete='SET NULL'), nullable=True)
    number = AppDb.Column(AppDb.Integer, nullable=False)  
    room = AppDb.Column(AppDb.String(65), nullable=False)
    code = AppDb.Column(AppDb.String(65), nullable=False)  # todo: Unique?

    # relationship(s)
    lab = AppDb.relationship('Laboratory', backref='freezer', lazy=True)

    def __repr__(self):
        return '<< Freezer: (number={0} || room={1} || lab={2} || code={3}) >>' \
            .format(self.number, self.room, self.laboratory_id, self.code)
