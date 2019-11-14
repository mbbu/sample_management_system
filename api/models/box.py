from api.models.database import BaseModel


class Box(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    tray_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('tray.id'))
    label = AppDb.Column(AppDb.String(65), nullable=False)

    # relationships
    sampleinbox = AppDb.relationship('Sample', backref='box', lazy='dynamic')

    def __repr__(self):
        return '<Box {}>'.format(self.label, self.tray_id)
