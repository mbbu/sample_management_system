from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.security_level import SecurityLevel
from api.resources.base_resource import BaseResource
from api.utils import format_and_lower_str, has_required_request_params, log_update, log_delete, \
    standard_non_empty_string, log_create, log_304


class SecurityLevelResource(BaseResource):
    fields = {
        'code': fields.String,
        'name': fields.String,
        'description': fields.String
    }

    def get(self):
        if request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
            security_level = SecurityLevelResource.get_security_level(code)
            if security_level is None:
                return BaseResource.send_json_message("Security level not found", 404)
            data = marshal(security_level, self.fields)
            return BaseResource.send_json_message(data, 200)
        else:
            security_level = SecurityLevel.query.all()
            if security_level is None:
                return BaseResource.send_json_message("Security levels not found", 404)
            data = marshal(security_level, self.fields)
            return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = SecurityLevelResource.security_level_parser()
        code = args['code']
        name = args['name']
        description = args['description']

        if not SecurityLevel.security_level_exists(code):
            try:
                security_level = SecurityLevel(code=code, name=name, description=description)
                BaseModel.db.session.add(security_level)
                BaseModel.db.session.commit()
                log_create(security_level)
                return BaseResource.send_json_message("Security level successfully created", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding security level", 500)
        current_app.logger.error("Error while adding security level :> Duplicate records")
        return BaseResource.send_json_message("Security level already exists", 409)

    @jwt_required
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        security_level = SecurityLevelResource.get_security_level(code)

        if security_level is None:
            current_app.logger.error("Error while updating security level. Record does not exist.")
            return BaseResource.send_json_message("Security level not found", 404)

        else:
            args = SecurityLevelResource.security_level_parser()
            code = args['code']
            name = args['name']
            description = args['description']

            if code != security_level.code or name != security_level.name or \
                    code != security_level.code or description != security_level.description:
                old_info = str(security_level)
                try:
                    security_level.name = name
                    security_level.code = code
                    security_level.description = description

                    BaseModel.db.session.commit()
                    log_update(old_info, security_level)
                    return BaseResource.send_json_message("Security level successfully updated", 202)
                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating security level", 500)
            log_304(security_level)
            return BaseResource.send_json_message("No changes made", 304)

    @jwt_required
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
        security_level = SecurityLevelResource.get_security_level(code)

        if security_level is None:
            return BaseResource.send_json_message("Security level not found", 404)
        BaseModel.db.session.delete(security_level)
        BaseModel.db.session.commit()
        log_delete(security_level)
        return BaseResource.send_json_message("Security level deleted", 200)

    @staticmethod
    def security_level_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True, type=standard_non_empty_string)
        parser.add_argument('name', required=True)
        parser.add_argument('description')

        args = parser.parse_args()
        return args

    @staticmethod
    def get_security_level(code):
        return BaseModel.db.session.query(SecurityLevel).filter_by(code=code).first()
