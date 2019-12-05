from api.models.database import BaseModel


class Publication(BaseModel.db.Model):
    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    sample_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('sample.id', ondelete='SET NULL'), nullable=True)
    user_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('users.id'), nullable=True)
    sample_results = AppDb.Column(AppDb.String(150), nullable=False)
    publication_title = AppDb.Column(AppDb.String(150), unique = True, nullable=True)
    co_authors = AppDb.Column(AppDb.String(150), nullable=True)

    # # todo: relationships defined here
    user= AppDb.relationship('User', back_populates='publication', uselist=False)

    @staticmethod
    def publication_exists(publication_title):
        if Publication.query.filter(
                Publication.publication_title == publication_title
        ).first():
            return True
        return False

    def __repr__(self):
        return '<Publication {}>'.format(self.sample_id, self.user_id, self.sample_results, self.publication_title,
                                         self.co_authors)
