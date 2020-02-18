from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, marshal, fields

from api.models.database import BaseModel
from api.models.role import Role
from api.resources.base_resource import BaseResource
from api.utils import format_and_lower_str, log_create, log_duplicate, \
    log_update, log_delete, has_required_request_params


class RoleResource(BaseResource):
    fields = {
        'code': fields.String,
        'name': fields.String,
        'description': fields.String
    }

    def get(self):
        if request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
            role = RoleResource.get_role(code)
            data = marshal(role, self.fields)
            return BaseResource.send_json_message(data, 200)
        else:
            roles = Role.query.all()
            data = marshal(roles, self.fields)
            return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = RoleResource.role_parser()
        code = format_and_lower_str(args['code'])
        name = args['name']
        description = args['description']

        if not Role.role_exists(code):
            try:
                role = Role(code=code, name=name, description=description)
                BaseModel.db.session.add(role)
                BaseModel.db.session.commit()
                log_create(role)
                return BaseResource.send_json_message("Added Role Successfully", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding role", 500)
        log_duplicate(Role.query.filter(Role.code == code).first())
        return BaseResource.send_json_message("Role already exists", 409)

    @jwt_required
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        role = RoleResource.get_role(code)

        if role is None:
            return BaseResource.send_json_message("Role not found", 404)

        else:
            args = RoleResource.role_parser()
            role_code = args['code']
            name = args['name']
            description = args['description']

            if role_code != role.code or name != role.name or description != role.description:
                try:
                    role.code = role_code
                    role.name = name
                    role.description = description
                    BaseModel.db.session.commit()
                    log_update(role, role)
                    return BaseResource.send_json_message("Updated Role Successfully", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating role", 500)
            return BaseResource.send_json_message("No changes made", 304)

    @jwt_required
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
        role = RoleResource.get_role(code)

        if not role:
            return BaseResource.send_json_message("Role not found", 404)

        BaseModel.db.session.delete(role)
        BaseModel.db.session.commit()
        log_delete(role)
        return BaseResource.send_json_message("Role deleted", 200)

    @staticmethod
    def role_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('description')

        args = parser.parse_args()
        return args

    @staticmethod
    def get_role(code):
        return BaseModel.db.session.query(Role).filter_by(code=code).first()
