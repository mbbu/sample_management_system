from api.models.database import BaseModel
from api.search.searchable_mixin import SearchableMixin


class Project(BaseModel.db.Model, SearchableMixin):
    __tablename__ = index_name = 'project'
    __searchable__ = ['code', 'name', 'description']

    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    code = AppDb.Column(AppDb.String(20), nullable=False, unique=True, index=True)
    theme_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('theme.id', ondelete='SET NULL'), nullable=False)
    name = AppDb.Column(AppDb.String(255), nullable=False, index=True)
    head = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('users.id', ondelete='SET NULL'), nullable=False)
    description = AppDb.Column(AppDb.String(255), nullable=True)

    # relationship(s) defined here
    samples = AppDb.relationship('Sample', backref='project', lazy=True)

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
