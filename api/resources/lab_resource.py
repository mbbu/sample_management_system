from flask import current_app

from flask_restful import marshal, reqparse, fields

from api.models.database import BaseModel
from api.resources.base_resource import BaseResource
from api.models.laboratory import Laboratory

class LaboratoryResource(BaseResource):
    fields = {
        'name' : fields.String,
        'room' : fields.String
    }

    def get(self):
        laboratory = Laboratory.query.all()
        data = marshal(laboratory, self.fields)
        return BaseResource.send_json_message(data, 200)

    def post(self):
        args = LaboratoryResource.laboratory_args()

        laboratory= Laboratory(
            name = args[0],
            room = args[1]
        ) 
        BaseModel.db.session.add(laboratory)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Succgitessfully Added Laboratory", 200)

    def put(self, name):
        laboratory = LaboratoryResource.get_laboratory(name)

        if not laboratory:
            return BaseResource.send_json_message("Laboratory does not exsist", 404)

        args = LaboratoryResource.laboratory_args()

        if args[0] != laboratory.name or args[2] != laboratory.room:
            try:
                laboratory.name = args[0]
                laboratory.room = args[1]
                BaseModel.db.session.commit()
                return BaseResource.send_json_message("Update was successful", 201)

            except Exception as e :
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while updationg Laboratory", 500)
        return BaseResource.send_json_message("No changes were made", 304)

    def delete(self, name):
        laboratory = LaboratoryResource.get_laboratory(name)

        if not laboratory:
            return BaseResource.send_json_message("Laboratory does not exsist", 404)
        BaseModel.db.session.delete(laboratory)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Laboratory successfully deleted", 200)

    @staticmethod
    def laboratory_args():
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('room', required=True)

        args = parser.parse_args()

        name = args['name']
        room = args['room']

        return [
            name, room
        ]

    @staticmethod
    def get_laboratory(name):
        return BaseModel.db.session.query(Laboratory).filter_by(name=name).first()
        
          


