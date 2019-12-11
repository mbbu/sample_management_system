from api.models.database import BaseModel


class Sample(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    theme_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('theme.id', ondelete='SET NULL'), nullable=True)
    user_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    box_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('box.id', ondelete='SET NULL'), nullable=True)
    animal_species = AppDb.Column(AppDb.String(100), nullable=False, index=True)
    sample_type = AppDb.Column(AppDb.String(100), nullable=True, index=True)
    sample_description = AppDb.Column(AppDb.String(150), nullable=True)
    location_collected = AppDb.Column(AppDb.String(100), nullable=True)
    project = AppDb.Column(AppDb.String(150), nullable=True, index=True)
    project_owner = AppDb.Column(AppDb.String(100), nullable=True)
    retention_period = AppDb.Column(AppDb.Integer, nullable=True)  # Default = Days
    barcode = AppDb.Column(AppDb.String(100), nullable=True)  # todo: changed to not nullable when module is done
    analysis = AppDb.Column(AppDb.String(100), nullable=True)
    temperature = AppDb.Column(AppDb.DECIMAL(5, 2), nullable=True)  # Default = Celsius
    amount = AppDb.Column(AppDb.Integer, nullable=True)  # todo set a default value
    code = AppDb.Column(AppDb.String, nullable=True)

    # relationship(s)
    user = AppDb.relationship('User', backref='sample', lazy=True)
    publication = AppDb.relationship('Publication', backref='sample', lazy=True)
    box = AppDb.relationship('Box', backref='sample', lazy=True)
    # todo: Add relationship between box and sample

    def __repr__(self):
        return '<< Sample: (type={0} || desc={1} || project={2} || barcode={3} || species={4} ||' \
            'box={5} || retention={6} || amount={7} || code={8} || location={9} || owner={10}'  \
            'analysis={11} || temperature={12} ) >>' \
        .format(self.sample_type, self.sample_description,
            self.project, self.barcode, self.animal_species,
            self.box_id, self.retention_period, self.amount, self.code,
            # not represented
            self.location_collected, self.project_owner,
            self.analysis, self.temperature)
