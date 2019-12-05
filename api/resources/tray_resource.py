from flask import current_app
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.tray import Tray
from api.resources.base_resource import BaseResource


class TrayResource(BaseResource):
    fields = {
        'number': fields.Integer,
        'rack.number': fields.Integer,
        'code': fields.String
    }

    def get(self):
        trays = Tray.query.all()
        data = marshal(trays, self.fields)
        return BaseResource.send_json_message(data, 200)

    def post(self):
        args = TrayResource.tray_parser()
        rack = int(args['rack'])
        number = int(args['number'])
        code = (args['code'])

        if not Tray.tray_exists(number):
            try:
                tray = Tray(rack_id=rack, number=number)
                BaseModel.db.session.add(tray)
                BaseModel.db.session.commit()
                return BaseResource.send_json_message("Added new tray", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding tray", 500)
        current_app.logger.error("Error while adding tray :> Duplicate records")
        return BaseResource.send_json_message("Tray already exists", 500)

    def put(self, code):
        args = TrayResource.tray_parser()
        rack = int(args['rack'])
        number = int(args['number'])
        code = (args['code'])

        tray = TrayResource.get_tray(code)
        if tray is not None:
            if rack != tray.rack_id or number != tray.number:
                try:
                    tray.rack_id = rack
                    tray.number = number
                    tray.code = code
                    BaseModel.db.session.commit()
                    return BaseResource.send_json_message("Updated tray", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding tray. Another tray has that number", 500)
            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("Tray not found", 404)

    def delete(self, code):
        tray = TrayResource.get_tray(code)

        if not tray:
            return BaseResource.send_json_message("Tray not found", 404)

        BaseModel.db.session.delete(tray)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Tray deleted", 200)

    @staticmethod
    def tray_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('rack', required=True)
        parser.add_argument('number', required=True)
        parser.add_argument('code', required=True)


        args = parser.parse_args()
        return args

    @staticmethod
    def get_tray(code):
        return BaseModel.db.session.query(Tray).filter_by(code=code).first()
