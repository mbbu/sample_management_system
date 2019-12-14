from api.models.database import BaseModel

class SecurityLevel(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
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
        return '<< SecurityLevel: (id={0} || code={1} || name={2} || description={3} )>>'.format(self.id, self.code, self.name, self.description)

