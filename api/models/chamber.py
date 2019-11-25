from api.models.database import BaseModel


class Chamber(BaseModel.db.Model):  # todo: what is the unique identifier.
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    freezer_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('freezer.id'))
    type = AppDb.Column(AppDb.String(50), nullable=False)
    code = AppDb.Column(AppDb.String(65), nullable=False)

    # relationship(s)
    freezer = AppDb.relationship('Freezer', backref='chamber', lazy=True)

    @staticmethod
    def chamber_exists(type):
        if Chamber.query.filter(
            Chamber.type == type
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< Chamber:  (type={0} || freezer={1} || code={2}) >>'.format(self.type, self.freezer_id, self.code)
