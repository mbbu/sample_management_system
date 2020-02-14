from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal, reqparse

from api.models.box import Box
from api.models.database import BaseModel
from api.resources.base_resource import BaseResource
from api.utils import format_and_lower_str, log_create, log_duplicate, log_update, log_delete, \
    has_required_request_params


class BoxResource(BaseResource):
    fields = {
        'label': fields.String,
        'code': fields.String,
        'tray.number': fields.Integer,
        'tray.rack.number': fields.Integer,
        'tray.rack.chamber.type': fields.String,
        'tray.rack.chamber.freezer.number': fields.Integer,
        'tray.rack.chamber.freezer.lab.name': fields.String,
        'tray.rack.chamber.freezer.lab.room': fields.Integer
    }

    def get(self):
        if request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])()
            box = BoxResource.get_box(code)
            if box is None:
                return BaseResource.send_json_message("Box not found", 404)
            data = marshal(box, self.fields)
            return BaseResource.send_json_message(data, 200)
        else:
            boxes = Box.query.all()
            if boxes is None:
                return BaseResource.send_json_message("Boxes not found", 404)
            data = marshal(boxes, self.fields)
            return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = BoxResource.box_args()
        code = format_and_lower_str(args[2])()

        if not Box.box_exists(code):
            try:
                box = Box(tray_id=args[0], label=args[1], code=args[2])

                BaseModel.db.session.add(box)
                BaseModel.db.session.commit()
                log_create(box)
                return BaseResource.send_json_message("Box successfully created", 201)
            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding box", 500)
        else:
            log_duplicate(Box)
            return BaseResource.send_json_message("Box already exists", 409)

    @jwt_required
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])()
        box = BoxResource.get_box(code)

        if box is None:
            return BaseResource.send_json_message("Box not found", 404)

        args = BoxResource.box_args()
        if args[0] != box.tray_id or args[1] != box.label or args[2] != box.code:
            try:
                box.tray_id = args[0]
                box.label = args[1]
                box.code = args[2]
                BaseModel.db.session.commit()
                log_update(box, box)
                return BaseResource.send_json_message("Box successfully updated", 202)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while updating box.", 500)
        return BaseResource.send_json_message("No changes made", 304)

    @jwt_required
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])()
        box = BoxResource.get_box(code)

        if not box:
            return BaseResource.send_json_message("Box not found", 404)

        BaseModel.db.session.delete(box)
        BaseModel.db.session.commit()
        log_delete(box)
        return BaseResource.send_json_message("Box deleted", 200)

    @staticmethod
    def box_args():
        parser = reqparse.RequestParser()
        parser.add_argument('tray', required=True)
        parser.add_argument('label', required=True)
        parser.add_argument('code', required=True)

        args = parser.parse_args()

        tray = args['tray']
        label = format_and_lower_str(args['label'])()
        code = format_and_lower_str(args['code'])()

        return [tray, label, code]

    @staticmethod
    def get_box(code):
        return BaseModel.db.session.query(Box).filter_by(code=code).first()
