from flask import current_app
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.rack import Rack
from api.resources.base_resource import BaseResource


class RackResource(BaseResource):
    fields = {
        'number': fields.Integer,
        'chamber.type': fields.String,
        'code': fields.String
    }

    def get(self):
        racks = Rack.query.all()
        data = marshal(racks, self.fields)
        return BaseResource.send_json_message(data, 200)

    def post(self):
        args = RackResource.rack_parser()
        chamber = int(args['chamber'])
        number = int(args['number'])
        code = (args['code'])

        if not Rack.rack_exists(number):
            try:
                rack = Rack(chamber_id=chamber, number=number, code=code)
                BaseModel.db.session.add(rack)
                BaseModel.db.session.commit()
                return BaseResource.send_json_message("Created new rack", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding tray", 500)
        current_app.logger.error("Error while adding tray :> Duplicate records")
        return BaseResource.send_json_message("Tray already exists", 500)

    def put(self, num):
        args = RackResource.rack_parser()
        chamber = int(args['chamber'])
        number = int(args['number'])
        code = (args['code'])

        rack = RackResource.get_rack(num)

        if rack is not None:
            if rack.chamber_id != chamber or rack.number != number or code.rack != code:
                try:
                    rack.chamber_id = chamber
                    rack.number = number
                    rack.code = code
                    BaseModel.db.session.commit()
                    return BaseResource.send_json_message("Updated rack", 202)
                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding tray. Another tray has that number", 500)
            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("Rack not found", 404)

    def delete(self, num):
        rack = RackResource.get_rack(num)

        if rack is None:
            return BaseResource.send_json_message("Rack not found", 404)
        BaseModel.db.session.delete(rack)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Rack deleted", 200)

    @staticmethod
    def rack_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('chamber', required=True)
        parser.add_argument('number', required=True)
        parser.add_argument('code', required=True)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_rack(num):
        return BaseModel.db.session.query(Rack).filter_by(number=num).first()
