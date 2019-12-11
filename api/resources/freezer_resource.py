from datetime import datetime

from flask import current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.freezer import Freezer
from api.resources.base_resource import BaseResource
from api.utils import format_and_lower_str, non_empty_int, non_empty_string


class FreezerResource(BaseResource):
    fields = {
        'number': fields.Integer,
        'room': fields.String,
        'lab.name': fields.String,
        'lab.room': fields.Integer,
        'code': fields.String
    }

    def get(self):
        if request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])()
            freezer = FreezerResource.get_freezer(code)
            data = marshal(freezer, self.fields)
            return BaseResource.send_json_message(data, 200)
        else:
            freezer = Freezer.query.all()
            data = marshal(freezer, self.fields)
            return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = FreezerResource.freezer_args()

        freezer = Freezer(
            laboratory_id=args[0],
            number=args[1],
            room=args[2],
            code=args[3]
        )

        BaseModel.db.session.add(freezer)
        BaseModel.db.session.commit()
        current_app.logger.info(
            "New {0} created by {1} at {2}".format(freezer, get_jwt_identity(), datetime.now()))
        return BaseResource.send_json_message("Freezer Successfully Created", 201)

    @jwt_required
    def put(self):
        args = FreezerResource.freezer_args()
        code = format_and_lower_str(args[3])()
        freezer = FreezerResource.get_freezer(code)

        if freezer is None:
            return BaseResource.send_json_message("Freezer does not exist", 404)

        elif args[0] != freezer.laboratory_id or args[1] != freezer.number or args[2] != freezer.room or args[
            3] != freezer.code:
            try:
                freezer.laboratory_id = args[0]
                freezer.number = args[1]
                freezer.room = args[2]
                freezer.code = args[3]
                BaseModel.db.session.commit()
                current_app.logger.info("{0} updated {1} to {2} at time={3}"
                                        .format(get_jwt_identity(), freezer, freezer,
                                                datetime.now()))
                return BaseResource.send_json_message("Successfully updated Freezer", 202)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while updating freezer", 500)
        else:
            return BaseResource.send_json_message("No changes made", 304)

    @jwt_required
    def delete(self):
        args = FreezerResource.freezer_args()
        code = format_and_lower_str(args[3])()
        freezer = FreezerResource.get_freezer(code)

        if freezer is None:
            return BaseResource.send_json_message("Freezer does not exist", 404)

        BaseModel.db.session.delete(freezer)
        BaseModel.db.session.commit()
        current_app.logger.info("{0} deleted {1} at {2}".format(get_jwt_identity(), freezer, datetime.now()))
        return BaseResource.send_json_message("Freezer deleted", 200)

    @staticmethod
    def freezer_args():
        parser = reqparse.RequestParser()
        parser.add_argument('laboratory', required=True)
        parser.add_argument('number', required=True, type=non_empty_int)
        parser.add_argument('room', required=True, type=non_empty_int)
        parser.add_argument('code', required=True, type=non_empty_string)

        args = parser.parse_args()

        laboratory = args['laboratory']
        number = args['number']
        room = args['room']
        code = format_and_lower_str(args['code'])()

        return [
            laboratory, number, room, code
        ]

    @staticmethod
    def get_freezer(code):
        return BaseModel.db.session.query(Freezer).filter_by(code=code).first()
