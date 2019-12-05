from flask import current_app
from flask_restful import fields, marshal, reqparse
from api.models.database import BaseModel
from api.resources.base_resource import BaseResource
from api.models.publication import Publication


class PublicationResource(BaseResource):
    fields = {
        'sample_id': fields.Integer,
        'user_id': fields.Integer,
        'sample_results': fields.String,
        'publication_title': fields.String,
        'co_authors': fields.String

    }

    def get(self):
        publications = Publication.query.all()
        data = marshal(publications, self.fields)
        return BaseResource.send_json_message(data, 200)

    def post(self):
        args = PublicationResource.publication_parser()
        sample_id = args['sample_id']
        user_id = args['user_id']
        sample_results = args['sample_results']
        publication_title = args['publication_title']
        co_authors = args['co_authors']

        if not Publication.publication_exists(publication_title):
            try:
                publication = Publication(
                    sample_id=sample_id,
                    user_id=user_id,
                    sample_results=sample_results,
                    publication_title=publication_title,
                    co_authors=co_authors
                )

                BaseModel.db.session.add(publication)
                BaseModel.db.session.commit()
                return BaseResource.send_json_message("Successfully Added a Publication", 200)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding publication", 500)
        current_app.logger.error("Error while adding Publication :> Duplicate records")
        return BaseResource.send_json_message('Publication already exists', 500)

    def put(self, publication_title):
        args = PublicationResource.publication_parser()

        sample_id = args['sample_id']
        user_id = args['user_id']
        sample_results = args['sample_results']
        publication_title = args['publication_title']
        co_authors = args['co_authors']

        publication = PublicationResource.get_publication(publication_title)

        if publication is not None:
            if sample_id != publication.sample_id or user_id != publication.user_id or \
                    sample_results != publication.sample_results or publication_title != publication.publication_title or \
                    co_authors != publication.co_authors:

                try:
                    publication.sample_id = sample_id,
                    publication.user_id = user_id,
                    publication.sample_results = sample_results,
                    publication.publication_title = publication_title,
                    publication.co_authors = co_authors

                    BaseModel.db.session.commit()
                    return BaseResource.send_json_message("Successfully Updated a Publication", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating publication", 500)
            current_app.logger.error("No changes were made", 304)
            return BaseResource.send_json_message("No changes found", 404)

    def delete(self, publication_title):
        publication = PublicationResource.get_publication(publication_title)

        if not publication:
            return BaseResource.send_json_message("Publication does not exist", 404)

        BaseModel.db.session.delete(publication)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Publication deleted", 200)

    @staticmethod
    def publication_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('sample_id')
        parser.add_argument('user_id')
        parser.add_argument('sample_results', required=True)
        parser.add_argument('publication_title', required=True)
        parser.add_argument('co_authors')

        args = parser.parse_args()
        return args

    @staticmethod
    def get_publication(publication_publication_title):
        return BaseModel.db.session.query(Publication).get(publication_)
