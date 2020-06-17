from api.models.database import BaseModel


class BioHazardLevel(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    code = AppDb.Column(AppDb.String(65), nullable=False)
    name = AppDb.Column(AppDb.String(65), nullable=True)
    description = AppDb.Column(AppDb.Text, nullable=True)

    # relationship(s) defined here

    @staticmethod
    def bio_hazard_level_exists(code):
        if BioHazardLevel.query.filter(
                BioHazardLevel.code == code
        ).first():
            return True
        return False

    def __repr__(self):
        return '<< BioHazardLevel: ( code={0} || name={1} || description={2} )>>'.format(self.code, self.name,
                                                                                         self.description)
