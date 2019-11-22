from flask import current_app
from flask_restful import fields, marshal, reqparse
from api.models.database import BaseModel
from api.models.freezer import Freezer
from api.resources.base_resource import BaseResource

class FreezerResource(BaseResource):
    fields = {
        'laboratory_id' : fields.Integer,
        'number' : fields.Integer,
        'room' : fields.String
    }

    def get(self):
        freezer = Freezer.query.all()
        data = marshal(freezer, self.fields)
        return BaseResource.send_json_message(data, 200)

    def post(self):
        args = FreezerResource.freezer_args()
        
        freezer = Freezer(
            laboratory_id= args[0],
            number = args[1],
            room = args[2]
        )

        BaseModel.db.session.add(freezer)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Freezer Sucessfully Created", 201)

    def put(self, number):
        freezer = FreezerResource.get_freezer(number)

        if not freezer:
            return BaseResource.send_json_message("Freezer does not exsist", 404)

        args = FreezerResource.freezer_args()

        if args[0] != freezer.laboratory_id or args[1] != freezer.number or args[2] != freezer.room:
            try:
                freezer.laboratory_id = args[0]
                freezer.number = args[1]
                freezer.room = args[2]
                return BaseResource.send_json_message("Sucessfully updated Freezer", 202)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while updating freezer", 500)
        return BaseResource.send_json_message("No changes made", 304)


    def delete(self, number):
        freezer = FreezerResource.get_freezer(number)

        if not freezer:
            return BaseResource.send_json_message("Freezer does not exsist", 404)

        BaseModel.db.session.delete(freezer)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Freezer deleted", 200)

    @staticmethod
    def freezer_args():
        parser = reqparse.RequestParser()
        parser.add_argument('laboratory_id', required=True)
        parser.add_argument('number', required=True)
        parser.add_argument('room', required=True)

        args = parser.parse_args()

        laboratory_id = args['laboratory_id']
        number = args['number']
        room = args['room']

        return [
            laboratory_id,number, room
        ]
    @staticmethod
    def get_freezer(number):
        return BaseModel.db.session.query(Freezer).filter_by(number=number).first()

        



    

