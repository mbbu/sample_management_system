from api.models.database import BaseModel


class Chamber(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    freezer_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('freezer.id'))
    type = AppDb.Column(AppDb.String(50), nullable=False)

    # relationship(s)
    freezer = AppDb.relationship('Freezer', backref='chamber', lazy=True)

    def __repr__(self):
        return '<< Chamber:  (type={0} || freezer={1}) >>'.format(self.type, self.freezer_id)
