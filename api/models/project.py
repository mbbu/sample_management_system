from api.models.database import BaseModel


class Project(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    code = AppDb.Column(AppDb.String(20), nullable=False, unique=True, index=True)
    theme_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('theme.id', ondelete='SET NULL'), nullable=False)
    description = AppDb.Column(AppDb.String(255), nullable=True)

    # relationship(s) defined here

    @staticmethod
    def project_exists(code):
        if Project.query.filter(
                Project.code == code
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< Project: (code={0} || theme={1} || description={2}) >>'.format(self.code, self.theme.name,
                                                                                  self.description)
