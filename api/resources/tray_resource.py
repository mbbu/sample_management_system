from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.tray import Tray
from api.resources.base_resource import BaseResource
from api.utils import format_and_lower_str, log_create, log_duplicate, log_update, log_delete, non_empty_string, \
    has_required_request_params


class TrayResource(BaseResource):
    fields = {
        'number': fields.Integer,
        'rack.number': fields.Integer,
        'code': fields.String
    }

    def get(self):
        if request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
            tray = TrayResource.get_tray(code)
            if tray is None:
                return BaseResource.send_json_message("Tray not found", 404)
            # else:
            data = marshal(tray, self.fields)
            return BaseResource.send_json_message(data, 200)
        else:
            trays = Tray.query.all()
            if trays is None:
                return BaseResource.send_json_message("Trays not found", 404)
            data = marshal(trays, self.fields)
            return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = TrayResource.tray_parser()
        rack = int(args['rack'])
        number = int(args['number'])
        code = format_and_lower_str(args['code'])

        if not Tray.tray_exists(code):
            try:
                tray = Tray(rack_id=rack, number=number, code=code)
                BaseModel.db.session.add(tray)
                BaseModel.db.session.commit()
                log_create(tray)
                return BaseResource.send_json_message("Tray successfully created", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding tray", 500)
        log_duplicate(Tray.query.filter(Tray.code == code).first())
        return BaseResource.send_json_message("Tray already exists", 409)

    @jwt_required
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        tray = TrayResource.get_tray(code)
        if tray is not None:
            args = TrayResource.tray_parser()
            rack = int(args['rack'])
            number = int(args['number'])
            code = format_and_lower_str(args['code'])

            if rack != tray.rack_id or number != tray.number or code != tray.code:
                try:
                    tray.rack_id = rack
                    tray.number = number
                    tray.code = code
                    BaseModel.db.session.commit()
                    log_update(tray, tray)  # todo: log old record
                    return BaseResource.send_json_message("Tray successfully updated", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding tray. Another tray has that number", 500)
            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("Tray not found", 404)

    @jwt_required
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
        tray = TrayResource.get_tray(code)

        if not tray:
            return BaseResource.send_json_message("Tray not found", 404)

        BaseModel.db.session.delete(tray)
        BaseModel.db.session.commit()
        log_delete(tray)
        return BaseResource.send_json_message("Tray deleted", 200)

    @staticmethod
    def tray_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('rack', required=True)
        parser.add_argument('number', required=True)
        parser.add_argument('code', required=True, type=non_empty_string)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_tray(code):
        return BaseModel.db.session.query(Tray).filter_by(code=code).first()
