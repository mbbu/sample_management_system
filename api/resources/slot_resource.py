import demjson  # used to decode javascript objects to py dicts
from flask import current_app
from flask_restful import marshal, fields, reqparse

from api import BaseResource
from api.models import Slot, Sample
from api.models.database import BaseModel
from api.utils import log_create, log_duplicate, get_query_params, fake


class SlotResource(BaseResource):
    fields = {
        'position': fields.String,
        'code': fields.String,
        'available': fields.Boolean,
        'box.tray.number': fields.String,
        'box.tray.rack.number': fields.String,
        'box.tray.rack.chamber.type': fields.String,
        'box.tray.rack.chamber.freezer.number': fields.String,
        'box.tray.rack.chamber.freezer.lab.name': fields.String,
        'box.tray.rack.chamber.freezer.lab.room': fields.String
    }

    def get(self):
        query_strings = get_query_params()
        if query_strings is not None:
            for query_string in query_strings:
                query, total = Slot.search(query_string, 1, 15)
                boxes = query.all()

                data = marshal(boxes, self.fields)
                return BaseResource.send_json_message(data, 200)
        else:
            slots = Slot.query.all()
            if slots is None:
                return BaseResource.send_json_message("Slots not found", 404)
            data = marshal(slots, self.fields)
            return BaseResource.send_json_message(data, 200)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('slots', required=True)
        args = parser.parse_args()
        slots = demjson.decode(args['slots'])
        return update_sample_in_slot(slots)

    @staticmethod
    def get_slot(code):
        return BaseModel.db.session.query(Slot).filter_by(code=code).first()


def create_slots(box, row, col):
    box = int(box)
    row = int(row)
    col = int(col)

    matrix = matrix_generator(row, col)

    for rc in matrix:
        for pos in rc:
            # auto-generate code
            code = fake.ean(length=8)

            if not Slot.slot_exists(code):
                try:
                    slot = Slot(box=box, code=code, pos=pos)

                    BaseModel.db.session.add(slot)
                    log_create(slot)
                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding slot", 500)
            else:
                log_duplicate(Slot.query.filter(Slot.code == code).first())
                return BaseResource.send_json_message("Slot already exists", 409)

    BaseModel.db.session.commit()  # commit once
    return BaseResource.send_json_message("Slots successfully created", 201)


def update_sample_in_slot(slots):
    """
        function takes a sample code for a given slot or list of samples for slots in a box
        and updates the sample code for the specified slot.
    """
    for slot in slots['updated']:
        updated_sample = BaseModel.db.session.query(Sample).filter_by(code=slot['old']).first()
        updated_sample.code = slot['new']  # set the new code of the sample

    BaseModel.db.session.commit()  # commit session once done
    return BaseResource.send_json_message("Samples in slots successfully updated", 201)


# function to create a matrix for the box to visualize the positions
def matrix_generator(row, col):
    return [[{'row': y + 1, 'col': x + 1} for x in range(col)] for y in range(row)]
