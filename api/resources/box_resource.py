from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal, reqparse

from api.models.box import Box
from api.models.database import BaseModel
from api.resources.base_resource import BaseResource
from api.resources.decorators.user_role_decorators import is_theme_admin
from api.resources.slot_resource import create_slots
from api.resources.tray_resource import TrayResource
from api.utils import format_and_lower_str, log_create, log_duplicate, log_update, log_delete, \
    has_required_request_params, non_empty_string, non_empty_int, standard_non_empty_string, log_304, get_query_params


class BoxResource(BaseResource):
    fields = {
        'label': fields.String,
        'code': fields.String,
        'tray.number': fields.String,
        'tray.rack.number': fields.String,
        'tray.rack.chamber.type': fields.String,
        'tray.rack.chamber.freezer.number': fields.String,
        'tray.rack.chamber.freezer.lab.name': fields.String,
        'tray.rack.chamber.freezer.lab.room': fields.String
    }

    def get(self):
        query_strings = get_query_params()
        if query_strings is not None:
            for query_string in query_strings:
                query, total = Box.search(query_string, 1, 15)

                if total == 0:
                    # find all box in the selected freezer.
                    data = []

                    boxes = Box.query.all()
                    for box in boxes:
                        if box.tray.rack.chamber.freezer.code == query_string:
                            # find all boxes that have a free slot.
                            slots = []
                            for slot in box.slots:
                                slots.append(
                                    {'code': slot.code, 'position': slot.position, 'available': slot.available})

                            # try update box; convert box from an SQLAlchemy model to an OrderedDict
                            box = marshal(box, self.fields)
                            box['slots'] = slots  # updated box by adding slots

                            # add modified box to data
                            data.append(box)
                        else:
                            pass
                else:
                    boxes = query.all()

                    data = marshal(boxes, self.fields)
                return BaseResource.send_json_message(data, 200)

        elif request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
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
    @is_theme_admin
    def post(self):
        args = BoxResource.box_args()
        tray = TrayResource.get_tray(args['tray']).id
        label = args['label']
        code = args['code']
        row = args['rows']
        col = args['cols']

        if not Box.box_exists(code):
            try:
                box = Box(tray_id=tray, label=label, code=code)

                BaseModel.db.session.add(box)
                # move changes from Python to the database’s transaction buffer in order to access the id
                BaseModel.db.session.flush()

                log_create(box)

                # create Slots for the new box
                create_slots(box.id, row, col)
                return BaseResource.send_json_message("Box successfully created", 201)
            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding box", 500)
        else:
            log_duplicate(Box.query.filter(Box.code == code).first())
            return BaseResource.send_json_message("Box already exists", 409)

    @jwt_required
    @is_theme_admin
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        box = BoxResource.get_box(code)

        if box is None:
            return BaseResource.send_json_message("Box not found", 404)

        args = BoxResource.box_args()
        tray = TrayResource.get_tray(args['tray']).id
        label = args['label']
        code = args['code']

        if tray != box.tray_id or label != box.label or code != box.code:
            old_info = str(box)
            try:
                box.tray_id = tray
                box.label = label
                box.code = code
                BaseModel.db.session.commit()
                log_update(old_info, box)
                return BaseResource.send_json_message("Box successfully updated", 202)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while updating box.", 500)
        log_304(box)
        return BaseResource.send_json_message("No changes made", 304)

    @jwt_required
    @is_theme_admin
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
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
        parser.add_argument('tray', required=True, type=non_empty_int)
        parser.add_argument('label', required=True, type=non_empty_string)
        parser.add_argument('code', required=True, type=standard_non_empty_string)
        parser.add_argument('rows', required=False, type=non_empty_int)
        parser.add_argument('cols', required=False, type=non_empty_int)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_box(code):
        return BaseModel.db.session.query(Box).filter_by(code=code).first()
