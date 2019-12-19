from api.models.database import BaseModel

class Metadata(BaseModel.db.session):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    user_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    education = AppDb.Column(AppDb.String(150), nullable=True )
    employment = AppDb.Column(AppDb.String(150), nullable=True)
    marital_status = AppDb.Column(AppDb.String(150), nullable=True)
    number_of_people = AppDb.Column(AppDb.Integer, nullable=True)
    number_of_children = AppDb.Column(AppDb.Integer, nullable=True)
    number_of_animals = AppDb.Column(AppDb.Integer, nullable=True)
    economic_activity = AppDb.Column(AppDb.String(250), nullable=True)
    type_of_animals = AppDb.Column(AppDb.String(250), nullable=True)
    farming_activities = AppDb.Column(AppDb.String(250), nullable=True)
    social_economic_data = AppDb.Column(AppDb.Boolean, nullable=False, default=False)

    #relationships
    user = AppDb.relationship('User', backref='metadata', lazy=True)

    def __repr__(self):
        return '<< Household_metadata: (education={0} || employment={1} || married={2} ||' \
                'people={3} || children={4} || animals={5} || economic_activity={6} || '\
                'animaltype={7} || farming_activities={8} || social_economic_data={9} ) >>' \
            .format(self.education, self.employment, self.marital_status, self.number_of_people,
                    self.number_of_children, self.number_of_animals, self.economic_activity,
                    self.type_of_animals, self.farming_activities,self.social_economic_data)




