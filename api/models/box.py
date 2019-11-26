from api.models.database import BaseModel


class Box(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    tray_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('tray.id'), nullable=True)
    label = AppDb.Column(AppDb.String(65), nullable=False)

    # relationship(s)
    tray = AppDb.relationship('Tray', backref='box', lazy=True)

    def __repr__(self):
        return '<< Box: (label={0} || tray={1}) >>'.format(self.label, self.tray_id)
