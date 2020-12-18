from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal, reqparse

from api.models.chamber import Chamber
from api.models.database import BaseModel
from api.resources.base_resource import BaseResource
from api.resources.decorators.user_role_decorators import is_theme_admin
from api.resources.freezer_resource import FreezerResource
from api.utils import format_and_lower_str, non_empty_string, log_create, log_duplicate, log_update, log_delete, \
    has_required_request_params, non_empty_int, standard_non_empty_string, log_304, get_query_params, fake, get_racks


class ChamberResource(BaseResource):
    fields = {
        'type': fields.String,
        'freezer.room': fields.String,
        'freezer.number': fields.String,
        'code': fields.String
    }

    def get(self):
        query_strings = get_query_params()
        if query_strings is not None:
            for query_string in query_strings:
                query, total = Chamber.search(query_string, 1, 15)

                # query freezer to check for chambers
                chamber = ChamberResource.get_chamber(query_string)

                if chamber is not None:
                    data = get_racks(chamber.id)
                    return BaseResource.send_json_message(data, 200)
                else:
                    chambers = query.all()

                data = marshal(chambers, self.fields)
                return BaseResource.send_json_message(data, 200)

        elif request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
            chamber = ChamberResource.get_chamber(code)
            if chamber is None:
                return BaseResource.send_json_message("Chamber not found", 404)
            else:
                data = marshal(chamber, self.fields)
                return BaseResource.send_json_message(data, 200)
        else:
            chambers = Chamber.query.all()
            if chambers is None:
                return BaseResource.send_json_message("Chambers not found", 404)
            else:
                data = marshal(chambers, self.fields)
                return BaseResource.send_json_message(data, 200)

    @jwt_required
    @is_theme_admin
    def post(self):
        args = ChamberResource.chamber_parser()
        if type(args['freezer']) is str:
            freezer = FreezerResource.get_freezer(args['freezer']).id
        else:
            freezer = args['freezer']

        _type = args['type']
        code = fake.ean(length=8)

        if not Chamber.chamber_exists(code):
            try:
                chamber = Chamber(freezer=freezer, _type=_type, code=code)
                BaseModel.db.session.add(chamber)
                BaseModel.db.session.commit()
                log_create(chamber)
                return BaseResource.send_json_message("Chamber successfully created", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding chamber", 500)
        else:
            log_duplicate(Chamber.query.filter(Chamber.code == code).first())
            return BaseResource.send_json_message("Chamber already exists", 409)

    @jwt_required
    @is_theme_admin
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        chamber = ChamberResource.get_chamber(code)

        if chamber is None:
            return BaseResource.send_json_message("Chamber not found", 404)

        else:
            args = ChamberResource.chamber_parser()
            if type(args['freezer']) is str:
                freezer_db = FreezerResource.get_freezer(args['freezer'])
                freezer = freezer_db.id
            else:
                freezer = args['freezer']
            _type = args['type']
            code = args['code']

            if chamber.freezer_id != freezer or chamber.type != _type or chamber.code != code:
                old_info = str(chamber)
                try:
                    chamber.freezer_id = freezer
                    chamber.type = _type
                    chamber.code = code
                    BaseModel.db.session.commit()
                    log_update(old_info, chamber)
                    return BaseResource.send_json_message("Chamber successfully updated", 202)
                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding Chamber. Another chamber has that type",
                                                          500)
            log_304(chamber)
            return BaseResource.send_json_message("No changes made", 304)

    @jwt_required
    @is_theme_admin
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
        chamber = ChamberResource.get_chamber(code)

        if chamber is None:
            return BaseResource.send_json_message("Chamber not found", 404)

        BaseModel.db.session.delete(chamber)
        BaseModel.db.session.commit()
        log_delete(chamber)
        return BaseResource.send_json_message("Chamber deleted", 200)

    @staticmethod
    def chamber_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('freezer', required=True, type=non_empty_int)
        parser.add_argument('type', required=True, type=non_empty_string)
        parser.add_argument('code', required=True, type=standard_non_empty_string)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_chamber(code):
        return BaseModel.db.session.query(Chamber).filter_by(code=code).first()

