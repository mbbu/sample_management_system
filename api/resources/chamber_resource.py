from datetime import datetime

from flask import current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import fields, marshal, reqparse

from api.models.chamber import Chamber
from api.models.database import BaseModel
from api.resources.base_resource import BaseResource
from api.utils import format_and_lower_str


class ChamberResource(BaseResource):
    fields = {
        'type': fields.String,
        'freezer.room': fields.String,
        'freezer.number': fields.String,
        'code': fields.String
    }

    def get(self):
        chambers = Chamber.query.all()
        data = marshal(chambers, self.fields)
        return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = ChamberResource.chamber_parser()
        freezer = int(args['freezer'])
        _type = args['type']
        code = args['code']

        if not Chamber.chamber_exists(code):
            try:
                chamber = Chamber(freezer_id=freezer, type=_type, code=code)
                BaseModel.db.session.add(chamber)
                BaseModel.db.session.commit()
                current_app.logger.info(
                    "New {0} created by {1} at {2}".format(chamber, get_jwt_identity(), datetime.now()))
                return BaseResource.send_json_message("Created new chamber", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding chamber", 500)
        current_app.logger.error("Error while adding chamber :> Duplicate records")
        return BaseResource.send_json_message("Chamber already exists", 500)

    @jwt_required
    def put(self):
        args = ChamberResource.chamber_parser()
        freezer = int(args['freezer'])
        _type = args['type']
        code = args['code']

        chamber = ChamberResource.get_chamber(code)

        if chamber is not None:
            if chamber.freezer_id != freezer or chamber.type != _type or code.chamber != code:
                try:
                    chamber.freezer_id = freezer
                    chamber.type = _type
                    chamber.commit = code
                    BaseModel.db.session.commit()
                    current_app.logger.info("{0} updated some info;"
                                            "freezer={1}, type={2}, code={3} at time={4}"
                                            .format(get_jwt_identity(), freezer, _type, code, datetime.now()))
                    return BaseResource.send_json_message("Updated chamber", 202)
                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding Chamber. Another chamber has that type",
                                                          500)
            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("Chamber not found", 404)

    @jwt_required
    def delete(self):
        code = format_and_lower_str(request.headers['code'])()
        chamber = ChamberResource.get_chamber(code)

        if chamber is None:
            return BaseResource.send_json_message("Chamber not found", 404)

        BaseModel.db.session.delete(chamber)
        BaseModel.db.session.commit()
        current_app.logger.info("{0} deleted {1} at {2}".format(get_jwt_identity(), chamber, datetime.now()))
        return BaseResource.send_json_message("Chamber deleted", 200)

    @staticmethod
    def chamber_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('freezer', required=True)
        parser.add_argument('type', required=True)
        parser.add_argument('code', required=True)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_chamber(code):
        return BaseModel.db.session.query(Chamber).filter_by(code=code).first()
