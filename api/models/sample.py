from api.models.database import BaseModel

class Sample (BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    user_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('users.id'))
    box_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('box.id'))
    animal_species = AppDb.Column(AppDb.String(100), nullable = False)
    sample_type = AppDb.Column(AppDb.String(100), nullable = False) 
    sample_description = AppDb.Column(AppDb.String(150), nullable = False)
    location_collected = AppDb.Column(AppDb.String(100), nullable = False)
    project = AppDb.Column(AppDb.String(150), nullable = False)
    project_owner = AppDb.Column(AppDb.String(100), nullable = False)
    retention_period = AppDb.Column(AppDb.Integer, nullable = True) #Default = Days
    barcode = AppDb.Column(AppDb.String(100), nullable = False)
    analysis = AppDb.Column(AppDb.String(100), nullable = True)
    temperature = AppDb.Column(AppDb.DECIMAL(5,2))
    amount = AppDb.Column(AppDb.Integer, nullable = False)

   # todo: relationships defined here
    boxhasSample = AppDb.relationship('Box', backref='box_sample', lazy= 'dynamic')

def __repr__(self) :
    return '<Sample {}>'.format( self.box_id, self.animal_species, self.sample_type, self.sample_description, self.location_collected,
        self.project, self.project_owner, self.retention_period, self.barcode, self.analysis, self.temperature, self.amount )
    