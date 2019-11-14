from api.models.database import BaseModel


class Chamber(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    freezer_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('freezer.id'))
    type = AppDb.Column(AppDb.String(50), nullable=False)

    # relationships
    chamberinrack = AppDb.relationship('Rack', backref='chamber', lazy='dynamic')

    def __repr__(self):
        return '<Chamber {}>'.format(self.freezer_id, self.type)
