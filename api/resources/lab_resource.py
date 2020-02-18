from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import marshal, reqparse, fields

from api.models.database import BaseModel
from api.models.laboratory import Laboratory
from api.resources.base_resource import BaseResource
from api.utils import format_and_lower_str, log_update, log_delete, log_duplicate, log_create, \
    has_required_request_params, standard_non_empty_string


class LaboratoryResource(BaseResource):
    fields = {
        'name': fields.String,
        'room': fields.String,
        'code': fields.String
    }

    def get(self):
        if request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
            lab = LaboratoryResource.get_laboratory(code)
            if lab is None:
                return BaseResource.send_json_message("Lab not found", 404)
            else:
                data = marshal(lab, self.fields)
                return BaseResource.send_json_message(data, 200)
        else:
            laboratory = Laboratory.query.all()
            if laboratory is None:
                return BaseResource.send_json_message("Lab not found", 404)
            else:
                data = marshal(laboratory, self.fields)
                return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = LaboratoryResource.laboratory_parser()

        name = args['name']
        room = args['room']
        code = args['code']

        if not Laboratory.code_exists(code):
            try:
                laboratory = Laboratory(
                    name=name,
                    room=room,
                    code=code
                )

                BaseModel.db.session.add(laboratory)
                BaseModel.db.session.commit()
                log_create(laboratory)
                return BaseResource.send_json_message("Successfully Added Laboratory", 200)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding Laboratory", 500)
        log_duplicate(Laboratory.query.filter(Laboratory.code == code).first())
        return BaseResource.send_json_message("Laboratory already exists", 409)

    @jwt_required
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        laboratory = LaboratoryResource.get_laboratory(code)
        old_info = laboratory

        if laboratory is None:
            return BaseResource.send_json_message("Lab not found", 404)

        else:
            args = LaboratoryResource.laboratory_parser()

            name = args['name']
            room = args['room']
            code = args['code']

            if name != laboratory.name or room != laboratory.room or code != laboratory.code:
                try:
                    laboratory.name = name
                    laboratory.room = room
                    laboratory.code = code
                    BaseModel.db.session.commit()
                    log_update(old_info, laboratory)
                    return BaseResource.send_json_message("Lab updated successfully", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating Laboratory", 500)
            return BaseResource.send_json_message("No changes were made", 304)

    @jwt_required
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
        laboratory = LaboratoryResource.get_laboratory(code)

        if laboratory is None:
            return BaseResource.send_json_message("Laboratory does not exist", 404)

        BaseModel.db.session.delete(laboratory)
        BaseModel.db.session.commit()
        log_delete(laboratory)
        return BaseResource.send_json_message("Laboratory successfully deleted", 200)

    @staticmethod
    def laboratory_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('room', required=True)
        parser.add_argument('code', required=True, type=standard_non_empty_string)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_laboratory(code):
        return BaseModel.db.session.query(Laboratory).filter_by(code=code).first()
