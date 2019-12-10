from datetime import datetime

from flask import current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import fields, marshal, reqparse

from api import BaseResource, BaseModel
from api.models import QuantityType
from api.utils import non_empty_string, format_and_lower_str


class QuantityTypeResource(BaseResource):
    fields = {
        'id': fields.String,
        'name': fields.String,
        'description': fields.String
    }

    def get(self):
        quantity_type = QuantityType.query.all()
        data = marshal(quantity_type, self.fields)
        return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = QuantityTypeResource.quantity_parser()
        _id = format_and_lower_str(args['code'])()
        name = args['name']
        description = args['description']

        if not QuantityType.exists(_id):
            try:
                quantity_type = QuantityType(id=_id, name=name, description=description)
                BaseModel.db.session.add(quantity_type)
                BaseModel.db.session.commit()
                current_app.logger.info(
                    "New {0} created by {1} at {2}".format(quantity_type, get_jwt_identity(), datetime.now()))
                return BaseResource.send_json_message("Added quantity type successfully", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding role", 500)
        current_app.logger.error("Error while adding role :> Duplicate records")
        return BaseResource.send_json_message("Role already exists", 500)

    @jwt_required
    def put(self):
        args = QuantityTypeResource.quantity_parser()
        _id = format_and_lower_str(args['code'])()
        name = args['name']
        description = args['description']

        quantity_type = QuantityTypeResource.get_quantity_type(_id)

        if quantity_type is not None:
            if _id != quantity_type.id or name != quantity_type.name or description != quantity_type.description:
                try:
                    quantity_type.id = _id
                    quantity_type.name = name
                    quantity_type.description = description

                    BaseModel.db.session.commit()
                    current_app.logger.info("{0} updated some info;"
                                            "id={1}, name={2}, description={3}at time={4}"
                                            .format(get_jwt_identity(), _id, name, description, datetime.now()))
                    return BaseResource.send_json_message("Updated quantity type", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating user. Another user has that email",
                                                          500)
            else:
                return BaseResource.send_json_message("No changes made", 304)
        else:
            current_app.logger.error("Error while updating quantity type. Record does not exist.")
            return BaseResource.send_json_message("Quantity type already exists", 500)

    @jwt_required
    def delete(self):
        _id = format_and_lower_str(request.headers['code'])()
        quantity_type = QuantityTypeResource.get_quantity_type(_id)

        if quantity_type is None:
            return BaseResource.send_json_message("Quantity type not found", 404)

        BaseModel.db.session.delete(quantity_type)
        BaseModel.db.session.commit()
        current_app.logger.info("{0} deleted {1} at {2}".format(get_jwt_identity(), quantity_type, datetime.now()))
        return BaseResource.send_json_message("Quantity Type Deleted", 200)

    @staticmethod
    def quantity_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True, type=non_empty_string)
        parser.add_argument('name', required=True)
        parser.add_argument('description')

        args = parser.parse_args()
        return args

    @staticmethod
    def get_quantity_type(_id):
        return BaseModel.db.session.query(QuantityType).filter_by(id=_id).first()
