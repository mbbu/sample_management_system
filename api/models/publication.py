from api.models.database import BaseModel
from api.search.searchable_mixin import SearchableMixin


class Publication(BaseModel.db.Model, SearchableMixin):
    __tablename__ = index_name = 'publication'
    __searchable__ = ['publication_title', 'co_authors']

    AppDb = BaseModel.db
    id = AppDb.Column(AppDb.Integer, primary_key=True)
    sample_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('sample.id', ondelete='SET NULL'), nullable=True)
    user_id = AppDb.Column(AppDb.Integer, AppDb.ForeignKey('users.id'), nullable=True)
    sample_results = AppDb.Column(AppDb.String(150), nullable=False)
    publication_title = AppDb.Column(AppDb.String(150), unique=True, nullable=False)
    co_authors = AppDb.Column(AppDb.String(150), nullable=True)

    # relationships defined here
    user = AppDb.relationship('User', back_populates='publication', uselist=False)

    @staticmethod
    def publication_exists(publication_title):
        if Publication.query.filter(
                Publication.publication_title == publication_title
        ).first():
            return True
        return False

    def __repr__(self):
        return '<Publication (sample={0} || user={1} || sample_results={2} || pub_title={3} || co_authors={4})>'.format(
            self.sample_id, self.user_id, self.sample_results, self.publication_title,
            self.co_authors)
