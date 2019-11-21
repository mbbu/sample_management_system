from flask import current_app
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.chamber import Chamber
from api.resources.base_resource import BaseResource


class ChamberResource(BaseResource):
    fields = {
        'freezer.room': fields.String,
        'freezer.number': fields.String,
        'type': fields.String
    }

    def get(self):
        chambers = Chamber.query.all()
        data = marshal(chambers, self.fields)
        return BaseResource.send_json_message(data, 200)

    def post(self):
        args = ChamberResource.chamber_parser()
        freezer = int(args['freezer'])
        _type = args['type']

        if not Chamber.chamber_exists(_type):
            try:
                chamber = Chamber(freezer_id=freezer, type=_type)
                BaseModel.db.session.add(chamber)
                BaseModel.db.session.commit()
                return BaseResource.send_json_message("Created new chamber", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding chamber", 500)
        current_app.logger.error("Error while adding tray :> Duplicate records")
        return BaseResource.send_json_message("Chamber already exists", 500)

    def put(self, c_type):
        args = ChamberResource.chamber_parser()
        freezer = int(args['freezer'])
        _type = args['type']

        chamber = ChamberResource.get_chamber(c_type)

        if chamber is not None:
            if chamber.freezer_id != freezer or chamber.type != _type:
                try:
                    chamber.freezer_id = freezer
                    chamber.type = _type
                    BaseModel.db.session.commit()
                    return BaseResource.send_json_message("Updated chamber", 202)
                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding Chamber. Another chamber has that type",
                                                          500)
            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("Chamber not found", 404)

    def delete(self, c_type):
        chamber = ChamberResource.get_chamber(c_type)

        if chamber is None:
            return BaseResource.send_json_message("Chamber not found", 404)
        BaseModel.db.session.delete(chamber)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Chamber deleted", 200)

    @staticmethod
    def chamber_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('freezer', required=True)
        parser.add_argument('type', required=True)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_chamber(c_type):
        return BaseModel.db.session.query(Chamber).filter_by(type=c_type).first()
