from api.models.database import BaseModel


class Laboratory(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    name = AppDb.Column(AppDb.String(65), nullable=False)
    room = AppDb.Column(AppDb.String(65), nullable=False)
    code = AppDb.Column(AppDb.String(65), nullable=False, unique=True)

    @staticmethod
    def code_exists(code):
        if Laboratory.query.filter(
                Laboratory.code == code
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< Laboratory: (name={0} || room={1} || code={2})  >>'.format(self.name, self.room, self.code)
