from datetime import datetime

from flask import current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import marshal, reqparse, fields

from api.models.database import BaseModel
from api.models.laboratory import Laboratory
from api.resources.base_resource import BaseResource
from api.utils import format_and_lower_str


class LaboratoryResource(BaseResource):
    fields = {
        'name': fields.String,
        'room': fields.String,
        'code': fields.String
    }

    def get(self):
        if request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])()
            lab = LaboratoryResource.get_laboratory(code)
            data = marshal(lab, self.fields)
            return BaseResource.send_json_message(data, 200)
        else:
            laboratory = Laboratory.query.all()
            data = marshal(laboratory, self.fields)
            return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = LaboratoryResource.laboratory_parser()

        name = args['name']
        room = args['room']
        code = format_and_lower_str(args['code'])()

        if not Laboratory.code_exists(code):
            try:
                laboratory = Laboratory(
                    name=name,
                    room=room,
                    code=code
                )

                BaseModel.db.session.add(laboratory)
                BaseModel.db.session.commit()
                current_app.logger.info(
                    "New {0} created by {1} at {2}".format(laboratory, get_jwt_identity(), datetime.now()))
                return BaseResource.send_json_message("Successfully Added Laboratory", 200)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding Laboratory")
        current_app.logger.error("Error while adding Laboratory :> Duplicate records")
        return BaseResource.send_json_message("Laboratory already exists")

    @jwt_required
    def put(self):
        args = LaboratoryResource.laboratory_parser()

        name = args['name']
        room = args['room']
        code = format_and_lower_str(args['code'])()

        laboratory = LaboratoryResource.get_laboratory(code)
        old_info = laboratory

        if laboratory is not None:
            if name != laboratory.name or room != laboratory.room or code != laboratory.code:
                try:
                    laboratory.name = name
                    laboratory.room = room
                    laboratory.code = code
                    BaseModel.db.session.commit()
                    current_app.logger.info("{0} updated {1} to {2} at time={3}"
                                            .format(get_jwt_identity(), old_info, laboratory,
                                                    datetime.now()))  # todo: check how to log old values and new values for a change
                    return BaseResource.send_json_message("Update was successful", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating Laboratory", 500)
        current_app.logger.error("No changes were made", 304)
        return BaseResource.send_json_message("No changes were made", 304)

    @jwt_required
    def delete(self):
        code = format_and_lower_str(request.headers['code'])()
        laboratory = LaboratoryResource.get_laboratory(code)

        if laboratory is None:
            return BaseResource.send_json_message("Laboratory does not exist", 404)

        BaseModel.db.session.delete(laboratory)
        BaseModel.db.session.commit()
        current_app.logger.info("{0} deleted {1} at {2}".format(get_jwt_identity(), laboratory, datetime.now()))
        return BaseResource.send_json_message("Laboratory successfully deleted", 200)

    @staticmethod
    def laboratory_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('room', required=True)
        parser.add_argument('code', required=True)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_laboratory(code):
        return BaseModel.db.session.query(Laboratory).filter_by(code=code).first()
