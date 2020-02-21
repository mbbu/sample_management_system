from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal, reqparse

from api import BaseResource, BaseModel
from api.models import QuantityType
from api.utils import non_empty_string, format_and_lower_str, log_delete, log_create, log_update, log_duplicate, \
    has_required_request_params, standard_non_empty_string, log_304


class QuantityTypeResource(BaseResource):
    fields = {
        'id': fields.String,
        'name': fields.String,
        'description': fields.String
    }

    def get(self):
        if request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
            quantity_type = QuantityTypeResource.get_quantity_type(code)
            if quantity_type is None:
                return BaseResource.send_json_message("Quantity type not found", 404)
            data = marshal(quantity_type, self.fields)
            return BaseResource.send_json_message(data, 200)
        else:
            quantity_type = QuantityType.query.all()
            if quantity_type is None:
                return BaseResource.send_json_message("Quantity types not found", 404)
            data = marshal(quantity_type, self.fields)
            return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = QuantityTypeResource.quantity_parser()
        _id = args['code']
        name = args['name']
        description = args['description']

        if not QuantityType.exists(_id):
            try:
                quantity_type = QuantityType(id=_id, name=name, description=description)
                BaseModel.db.session.add(quantity_type)
                BaseModel.db.session.commit()
                log_create(quantity_type)
                return BaseResource.send_json_message("Quantity type successfully created", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding quantity type", 500)
        log_duplicate(QuantityType.query.filter(QuantityType.id == _id).first())
        return BaseResource.send_json_message("Quantity type already exists", 409)

    @jwt_required
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        quantity_type = QuantityTypeResource.get_quantity_type(code)

        if quantity_type is None:
            return BaseResource.send_json_message("Quantity type not found", 404)
        else:
            args = QuantityTypeResource.quantity_parser()
            _id = args['code']
            name = args['name']
            description = args['description']

            if _id != quantity_type.id or name != quantity_type.name or description != quantity_type.description:
                old_info = str(quantity_type)
                try:
                    quantity_type.id = _id
                    quantity_type.name = name
                    quantity_type.description = description

                    BaseModel.db.session.commit()
                    log_update(old_info, quantity_type)
                    return BaseResource.send_json_message("Quantity type successfully updated", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating quantity type.", 500)
            log_304(quantity_type)
            return BaseResource.send_json_message("No changes made", 304)

    @jwt_required
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
        quantity_type = QuantityTypeResource.get_quantity_type(code)

        if quantity_type is None:
            return BaseResource.send_json_message("Quantity type not found", 404)

        BaseModel.db.session.delete(quantity_type)
        BaseModel.db.session.commit()
        log_delete(quantity_type)
        return BaseResource.send_json_message("Quantity type deleted", 200)

    @staticmethod
    def quantity_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True, type=standard_non_empty_string)
        parser.add_argument('name', required=True, type=non_empty_string)
        parser.add_argument('description')

        args = parser.parse_args()
        return args

    @staticmethod
    def get_quantity_type(_id):
        return BaseModel.db.session.query(QuantityType).filter_by(id=_id).first()
