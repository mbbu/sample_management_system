from flask import current_app
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.freezer import Freezer
from api.resources.base_resource import BaseResource


class FreezerResource(BaseResource):
    fields = {
        'number': fields.Integer,
        'room': fields.String,
        'lab.name': fields.String,
        'lab.room': fields.Integer,
        'code': fields.String
    }

    def get(self):
        freezer = Freezer.query.all()
        data = marshal(freezer, self.fields)
        return BaseResource.send_json_message(data, 200)

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
        return BaseResource.send_json_message("Freezer Successfully Created", 201)

    def put(self, number):
        freezer = FreezerResource.get_freezer(number)

        if not freezer:
            return BaseResource.send_json_message("Freezer does not exist", 404)
        args = FreezerResource.freezer_args()

        if args[0] != freezer.laboratory_id or args[1] != freezer.number or args[2] != freezer.room:
            try:
                freezer.laboratory_id = args[0]
                freezer.number = args[1]
                freezer.room = args[2]
                freezer.code = args[3]
                BaseModel.db.session.commit()
                return BaseResource.send_json_message("Successfully updated Freezer", 202)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while updating freezer", 500)
        return BaseResource.send_json_message("No changes made", 304)

    def delete(self, number):
        freezer = FreezerResource.get_freezer(number)

        if not freezer:
            return BaseResource.send_json_message("Freezer does not exist", 404)

        BaseModel.db.session.delete(freezer)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Freezer deleted", 200)

    @staticmethod
    def freezer_args():
        parser = reqparse.RequestParser()
        parser.add_argument('laboratory', required=True)
        parser.add_argument('number', required=True)
        parser.add_argument('room', required=True)
        parser.add_argument('code', required=True)

        args = parser.parse_args()

        laboratory = args['laboratory']
        number = args['number']
        room = args['room']
        code =args['code']

        return [
            laboratory, number, room, code
        ]

    @staticmethod
    def get_freezer(number):
        return BaseModel.db.session.query(Freezer).filter_by(number=number).first()
