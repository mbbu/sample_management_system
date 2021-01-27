from datetime import datetime

from sqlalchemy.orm import backref

from api.constants import SAMPLE_FROM_FIELD
from api.models.database import BaseModel
from api.search.searchable_mixin import SearchableMixin


class Sample(BaseModel.db.Model, SearchableMixin):
    __tablename__ = index_name = 'sample'
    __searchable__ = ['animal_species', 'sample_type', 'status',
                      'retention_date', 'barcode', 'analysis', 'code',
                      'temperature', 'bio_hazard_level', 'created_at']

    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    theme_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('theme.id', ondelete='CASCADE'),
                            nullable=False, index=True)
    user_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('users.id', ondelete='CASCADE'),
                           nullable=False, index=True)
    slot_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('slot.id', ondelete='CASCADE'),
                           nullable=False, index=True)
    animal_species = AppDb.Column(AppDb.String(100), nullable=True, index=True)
    sample_type = AppDb.Column(AppDb.String(100), nullable=True, index=True)
    sample_description = AppDb.Column(AppDb.Text, nullable=True)
    location_collected = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('study_block.id', ondelete='SET NULL'),
                                      nullable=True, index=True)
    project_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('project.id', ondelete='CASCADE'),
                              nullable=True, index=True)
    retention_date = AppDb.Column(AppDb.DateTime, nullable=True)
    barcode = AppDb.Column(AppDb.String(100), nullable=True)
    analysis = AppDb.Column(AppDb.String(100), nullable=True)
    temperature = AppDb.Column(AppDb.DECIMAL(5, 2), nullable=True)
    created_at = AppDb.Column(AppDb.DateTime, nullable=True, default=datetime.now)
    updated_at = AppDb.Column(AppDb.DateTime, nullable=True)
    deleted_at = AppDb.Column(AppDb.DateTime, nullable=True)
    deleted_by = AppDb.Column(AppDb.String(65), nullable=True)

    # Default = Celsius
    amount = AppDb.Column(AppDb.Integer, nullable=True, default=0)
    quantity_type = AppDb.Column(AppDb.String, AppDb.ForeignKey('quantity_type.id', ondelete='SET NULL'), nullable=True)
    bio_hazard_level = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('bio_hazard_level.id', ondelete='SET NULL'),
                                    nullable=True)
    code = AppDb.Column(AppDb.String, nullable=False, unique=True)
    status = AppDb.Column(AppDb.String, nullable=False, default=SAMPLE_FROM_FIELD)

    # relationship(s)
    slot = AppDb.relationship('Slot', backref=backref('sample', uselist=False), lazy=True)
    user = AppDb.relationship('User', backref='sample', lazy=True)
    requests = AppDb.relationship('SampleRequest', backref='requested_sample', lazy=True)
    publication = AppDb.relationship('Publication', backref='sample', lazy=True)
    quantity = AppDb.relationship('QuantityType', backref='quantity_type', lazy=True)
    bioHazardLevel = AppDb.relationship('BioHazardLevel', backref='sample', lazy=True)

    @staticmethod
    def sample_exists(code):
        if Sample.query.filter(
                Sample.code == code
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< Sample: (type={0} || desc={1} || project={2} || barcode={3} || species={4} ||' \
               'slot={5} || retention={6} || amount={7} || quantity={8} || code={9} || location={10} || owner={11}' \
               '|| analysis={12} || temperature={13} ) >>' \
            .format(self.sample_type, self.sample_description,
                    self.project, self.barcode, self.animal_species,
                    self.slot_id, self.retention_date, self.amount, self.quantity_type, self.code,
                    self.location_collected,
                    self.project_id, self.analysis, self.temperature)
