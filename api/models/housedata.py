from api.models.database import BaseModel
from api.search.searchable_mixin import SearchableMixin


class AnimalHealthHouseData(BaseModel.db.Model, SearchableMixin):
    __tablename__ = index_name = 'animal_health_house_data'
    __searchable__ = ['code', 'farmer', 'cattle_id']

    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    code = AppDb.Column(AppDb.String(20), nullable=False, unique=True, index=True)
    farmer = AppDb.Column(AppDb.String(30), nullable=False)
    cattle_id = AppDb.Column(AppDb.String(20), nullable=False)
    cattle_name = AppDb.Column(AppDb.String(20), nullable=False)
    cattle_color = AppDb.Column(AppDb.String(10), nullable=False)
    cattle_sex = AppDb.Column(AppDb.String, nullable=False)
    collar = AppDb.Column(AppDb.String, nullable=True)
    pcv = AppDb.Column(AppDb.String, nullable=True)  # packed cell volume
    diagnosis = AppDb.Column(AppDb.String, nullable=True)  # dx
    treatment = AppDb.Column(AppDb.String, nullable=True)  # rx
    cc = AppDb.Column(AppDb.String, nullable=True)
    notes = AppDb.Column(AppDb.Text, nullable=True)
    weight = AppDb.Column(AppDb.Float(precision=2), nullable=True)
    study_block_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('study_block.id', ondelete='SET NULL'), nullable=True)

    @staticmethod
    def house_data_exists(code):
        if AnimalHealthHouseData.query.filter(
                AnimalHealthHouseData.code == code
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< House Data: (code={0} || farmer={1} || cattle_id={2} || cattle_name={3} ||' \
               'color={4} || sex={5} || collar={6} || pcv={7} || dx={8} || rx={9} || ' \
               'cc={10} || notes={11} ) >>' \
            .format(self.code, self.farmer, self.cattle_id, self.cattle_name,
                    self.cattle_color, self.cattle_sex, self.collar,
                    self.pcv, self.diagnosis, self.treatment, self.cc, self.notes)
