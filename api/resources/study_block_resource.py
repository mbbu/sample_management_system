from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, fields, marshal

from api.models.database import BaseModel
from api.models.study_block import StudyBlock
from api.resources.base_resource import BaseResource
from api.utils import log_duplicate, log_304, format_and_lower_str, has_required_request_params, log_create, log_update, \
    standard_non_empty_string, non_empty_string, get_query_params


class StudyBlockResource(BaseResource):
    fields = {
        'area': fields.String, 'code': fields.String, 'name': fields.String
    }

    def get(self):
        query_strings = get_query_params()
        if query_strings is not None:
            for query_string in query_strings:
                query, total = StudyBlock.search(query_string, 1, 15)
                study_blocks = query.all()

                data = marshal(study_blocks, self.fields)
                return BaseResource.send_json_message(data, 200)

        elif request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
            study_block = StudyBlockResource.get_study_block(code)
            if study_block is None:
                return BaseResource.send_json_message("Study block not found", 404)
            else:
                data = marshal(study_block, self.fields)
                return BaseResource.send_json_message(data, 200)

        else:
            study_blocks = StudyBlock.query.all()
            if study_blocks is None:
                return BaseResource.send_json_message("Study blocks not found", 404)
            else:
                data = marshal(study_blocks, self.fields)
                return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = StudyBlockResource.study_block_parser()
        if not StudyBlock.study_block_exists(args['code']):
            try:
                study_block = StudyBlock()
                study_block = StudyBlockResource.save_data(study_block, args)

                BaseModel.db.session.add(study_block)
                BaseModel.db.session.commit()
                log_create(study_block)
                return BaseResource.send_json_message("Study block successfully created", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding study block", 500)
        log_duplicate(StudyBlock.query.filter(StudyBlock.code == args['code']).first())
        return BaseResource.send_json_message("Study block already exists", 409)

    @jwt_required
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers.get('code'))
        study_block = StudyBlockResource.get_study_block(code)

        if study_block is not None:
            args = StudyBlockResource.study_block_parser()

            if args['name'] != study_block.name or args['code'] != study_block.code or args['area'] != study_block.area:
                try:
                    old_info = str(study_block)
                    study_block = StudyBlockResource.save_data(study_block, args)
                    BaseModel.db.session.commit()
                    log_update(old_info, study_block)
                    return BaseResource.send_json_message("Study block successfully updated", 200)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating study block. Another study block has "
                                                          "that name or code", 500)
            log_304(study_block)
            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("Study block not found", 404)

    @jwt_required
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers.get('code'))
        study_block = StudyBlockResource.get_study_block(code)

        if not study_block:
            return BaseResource.send_json_message("Study block not found", 404)

        BaseModel.db.session.delete(study_block)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Study block deleted", 200)

    @staticmethod
    def study_block_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('area', required=True, type=non_empty_string)
        parser.add_argument('name', required=True, type=non_empty_string)
        parser.add_argument('code', required=True, type=standard_non_empty_string)

        args = parser.parse_args()
        return {
            'area': args['area'], 'name': args['name'], 'code': args['code']
        }

    @staticmethod
    def save_data(study_block, args):
        study_block.area, study_block.name, study_block.code = args['area'], args['name'], \
                                                               format_and_lower_str(args['code'])
        return study_block

    @staticmethod
    def get_study_block(code):
        return BaseModel.db.session.query(StudyBlock).filter_by(code=code).first()
