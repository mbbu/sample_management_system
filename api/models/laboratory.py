from api.models.database import BaseModel


class Laboratory(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    name = AppDb.Column(AppDb.String(65), nullable=False)
    room = AppDb.Column(AppDb.Integer, nullable=False)

    # relationships
    freezerinlab = AppDb.relationship('Freezer', backref='lab', lazy='dynamic')

    def __repr__(self):
        return '<Laboratory {}>'.format(self.name, self.room)
