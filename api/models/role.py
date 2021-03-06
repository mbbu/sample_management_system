from api.models.database import BaseModel


class Role(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    code = AppDb.Column(AppDb.String(20), nullable=False, unique=False, index=True)  # id on badge
    name = AppDb.Column(AppDb.String(50), nullable=False)  # predefined job
    description = AppDb.Column(AppDb.String(255), nullable=True)

    # relationship(s) defined here
    user = AppDb.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def role_exists(code):
        if Role.query.filter(
                Role.code == code
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< Role: (code={0} || name={1} || description={2}) >>'.format(self.code, self.name, self.description)
