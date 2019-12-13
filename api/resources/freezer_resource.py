from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.freezer import Freezer
from api.resources.base_resource import BaseResource
from api.utils import format_and_lower_str, non_empty_int, non_empty_string, log_create, has_required_request_params, \
    log_update, log_delete, log_duplicate


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
        code = format_and_lower_str(args[3])()

        if not Freezer.freezer_exists(code):
            try:
                freezer = Freezer(
                    laboratory_id=args[0],
                    number=args[1],
                    room=args[2],
                    code=code
                )

                BaseModel.db.session.add(freezer)
                BaseModel.db.session.commit()
                log_create(freezer)
                return BaseResource.send_json_message("Freezer Successfully Created", 201)
            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding freezer", 500)
        log_duplicate(Freezer.query.filter(Freezer.code == args[3]).first())
        return BaseResource.send_json_message("Freezer already exists", 500)

    @jwt_required
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])()
        freezer = FreezerResource.get_freezer(code)

        if freezer is None:
            return BaseResource.send_json_message("Freezer does not exist", 404)

        else:
            args = FreezerResource.freezer_args()
            if args[0] != freezer.laboratory_id or args[1] != freezer.number or args[2] != freezer.room or args[
                3] != freezer.code:
                try:
                    freezer.laboratory_id = args[0]
                    freezer.number = args[1]
                    freezer.room = args[2]
                    freezer.code = args[3]
                    BaseModel.db.session.commit()
                    log_update(freezer, freezer)
                    return BaseResource.send_json_message("Successfully updated Freezer", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating freezer", 500)
            return BaseResource.send_json_message("No changes made", 304)

    @jwt_required
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])()
        freezer = FreezerResource.get_freezer(code)

        if freezer is None:
            return BaseResource.send_json_message("Freezer does not exist", 404)

        BaseModel.db.session.delete(freezer)
        BaseModel.db.session.commit()
        log_delete(freezer)
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
