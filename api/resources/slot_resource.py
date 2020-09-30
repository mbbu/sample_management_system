from flask import current_app
from flask_jwt_extended import jwt_required
from faker import Faker

from api import BaseResource, BaseModel
from api.models import Slot
from api.resources.decorators.user_role_decorators import is_theme_admin
from api.utils import log_create, log_duplicate


class SlotResource(BaseResource):
    fake = Faker()

    def get(self):
        return BaseResource.send_json_message("Coming up soon", 200)


def create_slots(box, row, col):
    box = int(box)
    row = int(row)
    col = int(col)

    matrix = matrix_generator(row, col)

    for rc in matrix:
        for pos in rc:
            # auto-generate code
            code = SlotResource.fake.ean(length=8)

            if not Slot.slot_exists(code):
                try:
                    slot = Slot(box_id=box, code=code, position=pos)

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


# function to create a matrix for the box to visualize the positions
def matrix_generator(row, col):
    return [[{'row': y + 1, 'col': x + 1} for x in range(col)] for y in range(row)]

