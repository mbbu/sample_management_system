from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.housedata import AnimalHealthHouseData
from api.resources.base_resource import BaseResource
from api.resources.study_block_resource import StudyBlockResource
from api.utils import format_and_lower_str, log_create, log_update, log_delete, has_required_request_params, \
    log_duplicate, non_empty_int, get_query_params, fake


class HouseDataResource(BaseResource):
    fields = {
        'farmer': fields.String, 'cattle_id': fields.String,
        'cattle_sex': fields.String, 'collar': fields.String,
        'cattle_name': fields.String, 'cattle_color': fields.String,
        'pcv': fields.String, 'diagnosis': fields.String, 'treatment': fields.String,
        'cc': fields.String, 'notes': fields.String, 'code': fields.String, 'weight': fields.String,
        'study_block.name': fields.String, 'study_block.code': fields.String, 'study_block.area': fields.String,
        'date_collected': fields.DateTime
    }

    def get(self):
        query_strings = get_query_params()
        if query_strings is not None:
            for query_string in query_strings:
                query, total = AnimalHealthHouseData.search(query_string, 1, 15)
                samples = query.all()

                data = marshal(samples, self.fields)
                return BaseResource.send_json_message(data, 200)

        elif request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
            metadata = HouseDataResource.get_metadata(code)
            if metadata is None:
                return BaseResource.send_json_message("House data not found", 404)
            data = marshal(metadata, self.fields)
            return BaseResource.send_json_message(data, 200)
        else:
            house_metadata = AnimalHealthHouseData.query.all()
            if house_metadata is None:
                return BaseResource.send_json_message("House data not found", 404)
            data = marshal(house_metadata, self.fields)
            return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        code = fake.ean(length=8)

        if not AnimalHealthHouseData.house_data_exists(code):
            try:
                house_data = AnimalHealthHouseData()
                house_data = HouseDataResource.save_data(house_data, code)

                BaseModel.db.session.add(house_data)
                BaseModel.db.session.commit()
                log_create(house_data)
                return BaseResource.send_json_message("House data successfully created", 201)
            except Exception as e:
                print(e)
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding the house data", 500)
        log_duplicate(AnimalHealthHouseData.query.filter(AnimalHealthHouseData.code == code).first())
        return BaseResource.send_json_message("House data already exists", 409)

    @jwt_required
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        house_data = HouseDataResource.get_metadata(code)

        if house_data is not None:
            args = HouseDataResource.house_data_args()

            if house_data.farmer != args['farmer'] or house_data.cattle_id != args['cattle_id'] or \
                    house_data.cattle_name != args['cattle_name'] or house_data.cattle_color != args['cattle_color'] \
                    or house_data.weight != args['weight'] or \
                    house_data.cattle_sex != args['cattle_sex'] or house_data.diagnosis != args['diagnosis'] or \
                    house_data.collar != args['collar'] or house_data.treatment != args['treatment'] or \
                    house_data.pcv != args['pcv'] or house_data.notes != args['notes'] or house_data.cc != args['cc']:

                try:
                    old_info = str(house_data)

                    house_data = HouseDataResource.save_data(house_data, code)

                    BaseModel.db.session.commit()
                    log_update(old_info, house_data)
                    return BaseResource.send_json_message("House data successfully updated", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message(
                        "Error while adding metadata. Metadata with that name exists or "
                        "code", 500)

            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("House data not found", 404)

    @jwt_required
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
        house_metadata = HouseDataResource.get_metadata(code)

        if not house_metadata:
            return BaseResource.send_json_message("House data not found", 404)

        BaseModel.db.session.delete(house_metadata)
        BaseModel.db.session.commit()
        log_delete(house_metadata)
        return BaseResource.send_json_message("House data deleted", 200)

    @staticmethod
    def house_data_args():
        parser = reqparse.RequestParser()
        parser.add_argument('farmer', required=False, type=non_empty_int)
        parser.add_argument('cattle_id', required=False)
        parser.add_argument('cattle_name', required=False)
        parser.add_argument('cattle_color', required=False)
        parser.add_argument('cattle_sex', required=False)
        parser.add_argument('collar', required=False)
        parser.add_argument('pcv', required=False)
        parser.add_argument('diagnosis', required=False)
        parser.add_argument('treatment', required=False)
        parser.add_argument('cc', required=False)
        parser.add_argument('notes', required=False)
        parser.add_argument('study_block', required=False)
        parser.add_argument('weight', required=False)

        args = parser.parse_args()
        return {
            'farmer': args['farmer'], 'cattle_id': args['cattle_id'],
            'cattle_name': args['cattle_name'], 'cattle_color': args['cattle_color'],
            'cattle_sex': args['cattle_sex'], 'collar': args['collar'],
            'pcv': args['pcv'], 'diagnosis': args['diagnosis'], 'study_block': args['study_block'],
            'treatment': args['treatment'], 'cc': args['cc'], 'notes': args['notes'],
            'weight': args['weight']
        }

    @staticmethod
    def save_data(house_data, code):
        args = HouseDataResource.house_data_args()

        house_data.code, house_data.farmer = code, args['farmer']
        house_data.cattle_id, house_data.cattle_name = args['cattle_id'], args['cattle_name']
        house_data.cattle_color, house_data.cattle_sex = args['cattle_color'], args['cattle_sex']
        house_data.diagnosis, house_data.collar = args['diagnosis'], args['collar'],
        house_data.treatment, house_data.pcv = args['treatment'], args['pcv'],
        house_data.notes, house_data.cc = args['notes'], args['cc']
        house_data.weight = args['weight']
        house_data.study_block_id = StudyBlockResource.get_study_block(args['study_block']).id

        return house_data

    @staticmethod
    def get_metadata(code):
        return BaseModel.db.session.query(AnimalHealthHouseData).filter_by(code=code).first()
