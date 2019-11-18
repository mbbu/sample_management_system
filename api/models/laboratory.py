from api.models.database import BaseModel


class Laboratory(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    name = AppDb.Column(AppDb.String(65), nullable=False)
    room = AppDb.Column(AppDb.Integer, nullable=False)

    # relationship(s)
    freezer = AppDb.relationship('Freezer', backref='lab', lazy=True)

    def __repr__(self):
        return '<< Laboratory: (name={0} || room={1}) >>'.format(self.name, self.room)
