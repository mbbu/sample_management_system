from api.models.database import BaseModel


class Freezer(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    laboratory_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('laboratory.id'))
    freezer = AppDb.Column(AppDb.Integer, nullable=False)  # todo change freezer to number
    room = AppDb.Column(AppDb.String(65), nullable=False)

    # relationship(s)
    lab = AppDb.relationship('Laboratory', backref='freezer', lazy=True)
    #chamber = AppDb.relationship('Chamber', backref='freezer', lazy=True)

    def __repr__(self):
        return '<< Freezer: (number={0} || room={1} || lab={2}) >>'\
            .format(self.freezer, self.room, self.laboratory_id)
