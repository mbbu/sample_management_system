from flask import current_app

from flask_restful import marshal, reqparse, fields

from api.models.database import BaseModel
from api.resources.base_resource import BaseResource
from api.models.laboratory import Laboratory

class LaboratoryResource(BaseResource):
    fields = {
        'name' : fields.String,
        'room' : fields.String,
        'code' : fields.String
    }

    def get(self):
        laboratory = Laboratory.query.all()
        data = marshal(laboratory, self.fields)
        return BaseResource.send_json_message(data, 200)

    def post(self):
        args = LaboratoryResource.laboratory_parser()

        name = args['name']
        room = args['room']
        code = args['code']

        if not Laboratory.code_exists(code) :
            try:
                laboratory = Laboratory(
                    name = name,
                    room = room,
                    code = code
                )

                BaseModel.db.session.add(laboratory)
                BaseModel.db.session.commit()
                return BaseResource.send_json_message("Successfully Added Laboratory", 200)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding Laboratory")
        current_app.logger.error("Error while adding Laboratory :> Duplicate records")
        return BaseResource.send_json_message("Laboratory already exists")

    def put(self, code):
        args = LaboratoryResource.laboratory_parser()

        name = args['name']
        room = args['room']
        code = args['code']

        laboratory = LaboratoryResource.get_laboratory(code)

        if  laboratory is  not None:
            if name != laboratory.name or room != laboratory.room or code != laboratory.code:
                try:
                    laboratory.name = name
                    laboratory.room = room
                    laboratory.code = code

                    BaseModel.db.session.commit()
                    return BaseResource.send_json_message("Update was successful", 201)

                except Exception as e :
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updationg Laboratory", 500)
        current_app.logger.error("No changes were made", 304)
        return BaseResource.send_json_message("No changes were made", 304)

    def delete(self, code):
        laboratory = LaboratoryResource.get_laboratory(code)

        if not laboratory:
            return BaseResource.send_json_message("Laboratory does not exsist", 404)
        BaseModel.db.session.delete(laboratory)
        BaseModel.db.session.commit()
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
        
          


