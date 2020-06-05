from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal, reqparse

from api.models.bio_hazard_level import BioHazardLevel
from api.models.database import BaseModel
from api.resources.base_resource import BaseResource
from api.resources.decorators.user_role_decorators import is_theme_admin
from api.utils import format_and_lower_str, has_required_request_params, log_update, log_delete, \
    standard_non_empty_string, log_create, log_304


class BioHazardLevelResource(BaseResource):
    fields = {
        'code': fields.String,
        'name': fields.String,
        'description': fields.String
    }

    def get(self):
        if request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
            bio_hazard_level = BioHazardLevelResource.get_bio_hazard_level(code)
            if bio_hazard_level is None:
                return BaseResource.send_json_message("Bio Hazard level not found", 404)
            data = marshal(bio_hazard_level, self.fields)
            return BaseResource.send_json_message(data, 200)
        else:
            bio_hazard_level = BioHazardLevel.query.all()
            if bio_hazard_level is None:
                return BaseResource.send_json_message("Bio Hazard levels not found", 404)
            data = marshal(bio_hazard_level, self.fields)
            return BaseResource.send_json_message(data, 200)

    @jwt_required
    @is_theme_admin
    def post(self):
        args = BioHazardLevelResource.bio_hazard_level_parser()
        code = args['code']
        name = args['name']
        description = args['description']

        if not BioHazardLevel.bio_hazard_level_exists(code):
            try:
                bio_hazard_level = BioHazardLevel(code=code, name=name, description=description)
                BaseModel.db.session.add(bio_hazard_level)
                BaseModel.db.session.commit()
                log_create(bio_hazard_level)
                return BaseResource.send_json_message("Bio Hazard level successfully created", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding bio hazard level", 500)
        current_app.logger.error("Error while adding bio hazard level :> Duplicate records")
        return BaseResource.send_json_message("Bio Hazard level already exists", 409)

    @jwt_required
    @is_theme_admin
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        bio_hazard_level = BioHazardLevelResource.get_bio_hazard_level(code)

        if bio_hazard_level is None:
            current_app.logger.error("Error while updating bio hazard level. Record does not exist.")
            return BaseResource.send_json_message("Bio Hazard level not found", 404)

        else:
            args = BioHazardLevelResource.bio_hazard_level_parser()
            code = args['code']
            name = args['name']
            description = args['description']

            if code != bio_hazard_level.code or name != bio_hazard_level.name or \
                    code != bio_hazard_level.code or description != bio_hazard_level.description:
                old_info = str(bio_hazard_level)
                try:
                    bio_hazard_level.name = name
                    bio_hazard_level.code = code
                    bio_hazard_level.description = description

                    BaseModel.db.session.commit()
                    log_update(old_info, bio_hazard_level)
                    return BaseResource.send_json_message("Bio Hazard level successfully updated", 202)
                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating bio hazard level", 500)
            log_304(bio_hazard_level)
            return BaseResource.send_json_message("No changes made", 304)

    @jwt_required
    @is_theme_admin
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
        bio_hazard_level = BioHazardLevelResource.get_bio_hazard_level(code)

        if bio_hazard_level is None:
            return BaseResource.send_json_message("Bio Hazard level not found", 404)
        BaseModel.db.session.delete(bio_hazard_level)
        BaseModel.db.session.commit()
        log_delete(bio_hazard_level)
        return BaseResource.send_json_message("Bio Hazard level deleted", 200)

    @staticmethod
    def bio_hazard_level_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True, type=standard_non_empty_string)
        parser.add_argument('name', required=True)
        parser.add_argument('description')

        args = parser.parse_args()
        return args

    @staticmethod
    def get_bio_hazard_level(code):
        return BaseModel.db.session.query(BioHazardLevel).filter_by(code=code).first()
