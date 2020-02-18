from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.rack import Rack
from api.resources.base_resource import BaseResource
from api.utils import format_and_lower_str, log_create, log_duplicate, log_update, log_delete, non_empty_string, \
    has_required_request_params


class RackResource(BaseResource):
    fields = {
        'number': fields.Integer,
        'chamber.type': fields.String,
        'code': fields.String
    }

    def get(self):
        if request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
            rack = RackResource.get_rack(code)
            if rack is None:
                return BaseResource.send_json_message("Rack not found", 404)
            else:
                data = marshal(rack, self.fields)
                return BaseResource.send_json_message(data, 200)
        else:
            racks = Rack.query.all()
            if racks is None:
                return BaseResource.send_json_message("Racks not found", 404)
            else:
                data = marshal(racks, self.fields)
                return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = RackResource.rack_parser()
        chamber = int(args['chamber'])
        number = int(args['number'])
        code = format_and_lower_str(args['code'])

        if not Rack.rack_exists(code):
            try:
                rack = Rack(chamber_id=chamber, number=number, code=code)
                BaseModel.db.session.add(rack)
                BaseModel.db.session.commit()
                log_create(rack)
                return BaseResource.send_json_message("Rack successfully created", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding rack", 500)
        log_duplicate(Rack.query.filter(Rack.code == code).first())
        return BaseResource.send_json_message("Rack already exists", 409)

    @jwt_required
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        rack = RackResource.get_rack(code)

        if rack is not None:
            args = RackResource.rack_parser()
            chamber = int(args['chamber'])
            number = int(args['number'])
            code = format_and_lower_str(args['code'])

            if rack.chamber_id != chamber or rack.number != number or code.rack != code:
                try:
                    rack.chamber_id = chamber
                    rack.number = number
                    rack.code = code
                    BaseModel.db.session.commit()
                    log_update(rack, rack)  # todo: log old update
                    return BaseResource.send_json_message("Rack successfully updated", 202)
                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding rack. Another rack has that number", 500)
            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("Rack not found", 404)

    @jwt_required
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
        rack = RackResource.get_rack(code)

        if rack is None:
            return BaseResource.send_json_message("Rack not found", 404)
        BaseModel.db.session.delete(rack)
        BaseModel.db.session.commit()
        log_delete(rack)
        return BaseResource.send_json_message("Rack deleted", 200)

    @staticmethod
    def rack_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('chamber', required=True)
        parser.add_argument('number', required=True)
        parser.add_argument('code', required=True, type=non_empty_string)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_rack(code):
        return BaseModel.db.session.query(Rack).filter_by(code=code).first()
