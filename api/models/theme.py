from api.models.database import BaseModel


class Theme(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    code = AppDb.Column(AppDb.String(10), nullable=True, unique=True)
    name = AppDb.Column(AppDb.String(65), nullable=False, unique=True, index=True)

    # relationship
    sample = AppDb.relationship('Sample', backref='theme', lazy=True)
    projects = AppDb.relationship('Project', backref='theme', lazy=True)

    @staticmethod
    def theme_exists(code):
        if Theme.query.filter(
                Theme.code == code
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< Theme: (code={0} || name={1}) >>'.format(self.code, self.name)
