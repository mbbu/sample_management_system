from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal, reqparse

from api.models import Chamber, Rack, Tray
from api.models.database import BaseModel
from api.models.freezer import Freezer
from api.resources.base_resource import BaseResource
from api.resources.decorators.user_role_decorators import is_theme_admin
from api.resources.lab_resource import LaboratoryResource
from api.utils import format_and_lower_str, non_empty_int, log_create, has_required_request_params, \
    log_update, log_delete, log_duplicate, standard_non_empty_string, log_304, get_query_params, fake, get_chambers


class FreezerResource(BaseResource):
    fields = {
        'number': fields.String,
        'lab.building': fields.String,
        'lab.room': fields.String,
        'code': fields.String
    }

    def get(self):
        query_strings = get_query_params()
        if query_strings is not None:
            for query_string in query_strings:
                query, total = Freezer.search(query_string, 1, 15)

                # query freezer to check for chambers
                freezer = FreezerResource.get_freezer(query_string)

                if freezer is not None:
                    data = get_chambers(freezer.id)
                    return BaseResource.send_json_message(data, 200)
                else:
                    freezers = query.all()

                data = marshal(freezers, self.fields)
                return BaseResource.send_json_message(data, 200)

        elif request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
            freezer = FreezerResource.get_freezer(code)
            if freezer is None:
                return BaseResource.send_json_message("Freezer not found", 404)
            else:
                data = marshal(freezer, self.fields)
                return BaseResource.send_json_message(data, 200)
        else:
            freezer = Freezer.query.all()
            if freezer is None:
                return BaseResource.send_json_message("Freezers not found", 404)
            else:
                data = marshal(freezer, self.fields)
                return BaseResource.send_json_message(data, 200)

    @jwt_required
    @is_theme_admin
    def post(self):
        args = FreezerResource.freezer_args()
        if type(args['laboratory']) is str:
            lab = LaboratoryResource.get_laboratory(args['laboratory']).id
        else:
            lab = args['laboratory']

        number = args['number']
        code = fake.ean(length=8)
        chambers = int(args['chambers'])
        racks = int(args['racks'])
        trays = int(args['trays'])

        if not Freezer.freezer_exists(code):
            try:
                freezer = Freezer(lab=lab, num=number, code=code)
                BaseModel.db.session.add(freezer)  # add freezer to session
                BaseModel.db.session.flush()  # flush session to make it available for reference even b4 commit

                # create other resources
                for _ in range(chambers):
                    number = _ + 1
                    chamber = Chamber(freezer=freezer.id, _type=number, code=fake.ean(length=8))
                    BaseModel.db.session.add(chamber)
                    BaseModel.db.session.flush()
                    for _ in range(racks):
                        num = _ + 1
                        rack = Rack(chamber=chamber.id, num=num, code=fake.ean(length=8))
                        BaseModel.db.session.add(rack)
                        BaseModel.db.session.flush()
                        for _ in range(trays):
                            nums = _ + 1
                            tray = Tray(rack=rack.id, num=nums, code=fake.ean(length=8))
                            BaseModel.db.session.add(tray)
                            BaseModel.db.session.flush()

                BaseModel.db.session.commit()
                log_create(freezer)
                return BaseResource.send_json_message("Freezer Successfully Created", 201)
            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding freezer", 500)
        log_duplicate(Freezer.query.filter(Freezer.code == code).first())
        return BaseResource.send_json_message("Freezer already exists", 409)

    @jwt_required
    @is_theme_admin
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        freezer = FreezerResource.get_freezer(code)

        if freezer is None:
            return BaseResource.send_json_message("Freezer does not exist", 404)

        else:
            args = FreezerResource.freezer_args()
            if type(args['laboratory']) is str:
                lab = LaboratoryResource.get_laboratory(args['laboratory'])
                laboratory = lab.id
            else:
                laboratory = args['laboratory']

            number = args['number']
            code = args['code']

            if laboratory != freezer.laboratory_id or number != freezer.number or \
                    code != freezer.code:
                old_info = str(freezer)
                try:
                    freezer.laboratory_id = laboratory
                    freezer.number = number
                    freezer.code = code
                    BaseModel.db.session.commit()
                    log_update(old_info, freezer)
                    return BaseResource.send_json_message("Successfully updated freezer", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating freezer", 500)
            log_304(freezer)
            return BaseResource.send_json_message("No changes made", 304)

    @jwt_required
    @is_theme_admin
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
        freezer = FreezerResource.get_freezer(code)

        if freezer is None:
            return BaseResource.send_json_message("Freezer does not exist", 404)

        BaseModel.db.session.delete(freezer)
        BaseModel.db.session.commit()
        log_delete(freezer)
        return BaseResource.send_json_message("Freezer deleted", 200)

    @staticmethod
    def freezer_args():
        parser = reqparse.RequestParser()
        parser.add_argument('laboratory', required=True, type=non_empty_int)
        parser.add_argument('number', required=True, type=non_empty_int)
        parser.add_argument('code', required=True, type=standard_non_empty_string)
        parser.add_argument('chambers', required=False, type=non_empty_int)
        parser.add_argument('racks', required=False, type=non_empty_int)
        parser.add_argument('trays', required=False, type=non_empty_int)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_freezer(code):
        return BaseModel.db.session.query(Freezer).filter_by(code=code).first()
