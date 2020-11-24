from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.publication import Publication
from api.resources.base_resource import BaseResource
from api.resources.decorators.user_role_decorators import is_publication_owner
from api.resources.sample_resource import SampleResource
from api.utils import log_create, log_duplicate, log_update, log_delete, format_and_lower_str, \
    has_required_request_params, non_empty_int, log_304, get_any_user_by_email, get_query_params


class PublicationResource(BaseResource):
    fields = {
        'sample.project': fields.String,
        'sample.theme.name': fields.String,
        'sample.code': fields.String,
        'user.first_name': fields.String,
        'user.last_name': fields.String,
        'user.email': fields.String,
        'sample_results': fields.String,
        'publication_title': fields.String,
        'co_authors': fields.String

    }

    def get(self):
        query_strings = get_query_params()
        if query_strings is not None:
            for query_string in query_strings:
                query, total = Publication.search(query_string, 1, 15)
                publications = query.all()

                data = marshal(publications, self.fields)
                return BaseResource.send_json_message(data, 200)

        elif request.headers.get('title') is not None:
            title = format_and_lower_str(request.headers['title'])
            publication = PublicationResource.get_publication(title)
            if publication is None:
                return BaseResource.send_json_message("Publication not found", 404)
            data = marshal(publication, self.fields)
            return BaseResource.send_json_message(data, 200)
        else:
            publications = Publication.query.all()
            if publications is None:
                return BaseResource.send_json_message("Publications not found", 404)
            data = marshal(publications, self.fields)
            return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = PublicationResource.publication_parser()
        sample_id = SampleResource.get_sample(args['sample']).id
        user_id = get_any_user_by_email(args['user']).id
        sample_results = args['sample_results']
        publication_title = format_and_lower_str(args['publication_title'])
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
                log_create(publication)
                return BaseResource.send_json_message("Publication successfully created", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding publication", 500)
        log_duplicate(Publication.query.filter(Publication.publication_title == publication_title).first())
        return BaseResource.send_json_message('Publication already exists', 409)

    @jwt_required
    @is_publication_owner
    @has_required_request_params
    def put(self):
        pub_title = format_and_lower_str(request.headers['title'])
        publication = PublicationResource.get_publication(pub_title)

        if publication is not None:
            args = PublicationResource.publication_parser()
            sample = SampleResource.get_sample(args['sample']).id
            user = get_any_user_by_email(args['user']).id
            sample_results = args['sample_results']
            publication_title = format_and_lower_str(args['publication_title'])
            co_authors = args['co_authors']

            if sample != publication.sample_id or user != publication.user_id or \
                    sample_results != publication.sample_results or publication_title != publication.publication_title \
                    or co_authors != publication.co_authors:
                old_info = str(publication)
                try:
                    publication.sample_id = sample
                    publication.user_id = user
                    publication.sample_results = sample_results
                    publication.publication_title = publication_title
                    publication.co_authors = co_authors

                    BaseModel.db.session.commit()
                    log_update(old_info, publication)
                    return BaseResource.send_json_message("Publication successfully updated", 200)
                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating publication", 500)
            log_304(publication)
            return BaseResource.send_json_message('No changes were made', 304)
        return BaseResource.send_json_message('Publication not found', 404)

    @jwt_required
    @is_publication_owner
    @has_required_request_params
    def delete(self):
        pub_title = format_and_lower_str(request.headers['title'])
        publication = PublicationResource.get_publication(pub_title)

        if not publication:
            return BaseResource.send_json_message("Publication not found", 404)

        BaseModel.db.session.delete(publication)
        BaseModel.db.session.commit()
        log_delete(publication)
        return BaseResource.send_json_message("Publication deleted", 200)

    @staticmethod
    def publication_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('sample', type=non_empty_int)
        parser.add_argument('user', type=non_empty_int)
        parser.add_argument('sample_results', required=False)
        parser.add_argument('publication_title', required=True)
        parser.add_argument('co_authors', required=False)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_publication(title):
        return BaseModel.db.session.query(Publication) \
            .filter_by(publication_title=title).first()
