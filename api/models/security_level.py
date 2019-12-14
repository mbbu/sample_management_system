from api.models.database import BaseModel

class SecurityLevel(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.String(65), primary_key=True)
    code = AppDb.Column(AppDb.String(65), nullable=True)
    name = AppDb.Column(AppDb.String(65), nullable=True)
    description = AppDb.Column(AppDb.String(65), nullable=True)

    @staticmethod
    def exists(code):
        if SecurityLevel.query.filter(
            SecurityLevel.code == code
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< SecurityLevel: (code={0} || name={1} || description={2} )>>'.format(self.code, self.name, self.description)

