from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.housedata import Housedata
from api.resources.base_resource import BaseResource
from api.utils import format_and_lower_str, log_create, log_update, log_delete, log_duplicate, \
    has_required_request_params

class HousedataResource(BaseResource):
    fields = {
        'user': fields.Integer,
        'education': fields.String,
        'employment': fields.String,
        'marital_status': fields.String,
        'people': fields.Integer,
        'children': fields.Integer,
        'animals': fields.Integer,
        'economic_activity': fields.String,
        'animaltype': fields.String,
        'farming_activities': fields.String,
        'social_economic_data': fields.Boolean,
        'code': fields.String
    }

    def get(self):
            if request.headers.get('label') is not None:
                code = format_and_lower_str(request.headers['code'])()
                metadata = HousedataResource.get_meatadata(code)
                data = marshal(metadata, self.fields)
                return BaseResource.send_json_message(data, 200)
            else:
                house_metadata = Housedata.query.all()
                data = marshal(house_metadata, self.fields)
                return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = HousedataResource.metadata_args()
        code = format_and_lower_str(args[11])()

        if not Housedata.housedata_exists(code):
            try:
                house_data = Housedata(user_id=args[0], education=args[1], employment=args[2],
                                 marital_status=args[3], number_of_people=args[4], number_of_children=args[5],
                                 number_of_animals=args[6], economic_activity=args[7], type_of_animals=args[8],
                                 farming_activities=args[9], social_economic_data=bool(args[10]), code=args[11])

                BaseModel.db.session.add(house_data)
                BaseModel.db.session.commit()
                log_create(house_data)
                return BaseResource.send_json_message("Metadata added successfully", 201)
            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding the Metadata", 500)
        log_duplicate(Housedata.query.filter(Housedata.code == code).first())
        return BaseResource.send_json_message("Metadata already exists", 500)

    @jwt_required
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])()
        house_data = Housedata.get_metadata(code)

        if house_data is not None:
            args = HousedataResource.metadata_args()
            if args[0] != house_data.user_id or args[1] != house_data.education or args[2] != house_data.employment or \
                args[3] != house_data.marital_status or args[4] != house_data.number_of_people or args[5] != house_data.number_of_children or \
                args[6] != house_data.number_of_animals or args[7] != house_data.economic_activity or \
                args[8] != house_data.type_of_animals or args[9] != house_data.farming_activities or  \
                args[10] != house_data.social_economic_data or args[11] != house_data.code :

                try:
                    house_data.user_id = args[0]
                    house_data.education = args[1]
                    house_data.employment = args[2]
                    house_data.marital_status = args[3]
                    house_data.number_of_people = args[4]
                    house_data.number_of_children = args[5]
                    house_data.number_of_animals = args[6]
                    house_data.economic_activity = args[7]
                    house_data.type_of_animals = args[8]
                    house_data.farming_activities = args[9]
                    house_data.social_economic_data = bool(args[10])
                    house_data.code = args[11]

                    BaseModel.db.session.commit()
                    log_update(house_data, house_data)
                    return BaseResource.send_json_message("Updated the Metadata", 202)

                except Exception as e:
                            current_app.logger.error(e)
                            BaseModel.db.session.rollback()
                            return BaseResource.send_json_message("Error while adding metadata. Metadata with that name exists or "
                                                                  "code", 500)

            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("Metadata not found", 404)

    @jwt_required
    @has_required_request_params
    def __delete__(self):
        code = format_and_lower_str(request.headers['code'])()
        house_metadata = HousedataResource.get_metadata(code)

        if not house_metadata:
            return BaseResource.send_json_message("Metadata does not exists")

        BaseModel.db.session.delete(house_metadata)
        BaseModel.db.session.commit()
        log_delete(house_metadata)
        return BaseResource.send_json_message("Metadata deleted successfully")

    @staticmethod
    def metadata_args():
        parser = reqparse.RequestParser()
        parser.add_argument('user', required=False)
        parser.add_argument('education', required=False)
        parser.add_argument('employment', required=False)
        parser.add_argument('marital_status', required=False)
        parser.add_argument('people', required=False)
        parser.add_argument('children', required=False)
        parser.add_argument('animals', required=False)
        parser.add_argument('economic_activity', required=False)
        parser.add_argument('type_of_animals', required=False)
        parser.add_argument('farming_activities', required=False)
        parser.add_argument('social_economic_data', required=False)
        parser.add_argument('code', required=False)

        args = parser.parse_args()

        user_id = int(args['user'])
        education = args['education']
        employment = args['employment']
        marital_status = args['marital_status']
        number_of_people = args['people']
        number_of_children = args['children']
        number_of_animals = args['animals']
        economic_activity = args['economic_activity']
        type_of_animals = args['type_of_animals']
        farming_activities = args['farming_activities']
        social_economic_data = args['social_economic_data']
        code = args['code']

        return [
            user_id, education,employment,marital_status,number_of_people,
            number_of_children, number_of_animals, economic_activity, type_of_animals,
            farming_activities, social_economic_data, code
        ]

    @staticmethod
    def get_metadata(code):
        return BaseModel.db.session.query(Housedata).filter_by(code=code).first()









