from flask import current_app

from api.models.database import BaseModel
from api.models.box import Box
from api.resources.base_resource import BaseResource

from flask_restful import fields, marshal, reqparse


class BoxResource(BaseResource):
    fields = {
        'label': fields.String,
        'tray.number': fields.Integer,
        'tray.rack.number': fields.Integer,
        'tray.rack.chamber.type': fields.String,
        'tray.rack.chamber.freezer.number': fields.Integer,
        'tray.rack.chamber.freezer.lab.name': fields.String,
        'tray.rack.chamber.freezer.lab.room': fields.Integer
    }

    def get(self):
        box = Box.query.all()
        data = marshal(box, self.fields)
        return BaseResource.send_json_message(data, 200)

    def post(self):
        args = BoxResource.box_args()

        box = Box(
            tray_id=args[0],
            label=args[1]
        )

        BaseModel.db.session.add(box)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Box created.", 201)

    def put(self, label):
        box = BoxResource.get_box(label)

        if not box:
            return BaseResource.send_json_message("Box not found", 404)
        args = BoxResource.box_args()

        if args[0] != box.tray_id or args[1] != box.label:
            try:
                box.tray_id = args[0]
                box.label = args[1]
                BaseModel.db.session.commit()
                return BaseResource.send_json_message("Updated box", 202)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while updating box.", 500)
        return BaseResource.send_json_message("No changes made", 304)

    def delete(self, label):
        box = BoxResource.get_box(label)

        if not box:
            return BaseResource.send_json_message("Box not found", 404)

        BaseModel.db.session.delete(box)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Box deleted", 200)

    @staticmethod
    def box_args():
        parser = reqparse.RequestParser()
        parser.add_argument('tray', required=True)
        parser.add_argument('label', required=True)

        args = parser.parse_args()

        tray = args['tray']
        label = args['label']

        return [
            tray, label
        ]

    @staticmethod
    def get_box(label):
        return BaseModel.db.session.query(Box).filter_by(label=label).first()
