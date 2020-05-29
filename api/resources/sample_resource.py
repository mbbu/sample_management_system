from datetime import datetime

from flask import current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.sample import Sample
from api.resources.base_resource import BaseResource
from api.resources.box_resource import BoxResource
from api.resources.decorators.user_role_decorators import is_sample_owner
from api.resources.quantity_type_resource import QuantityTypeResource
from api.resources.security_level_resource import SecurityLevelResource
from api.resources.theme_resource import ThemeResource
from api.utils import format_and_lower_str, log_create, log_update, log_duplicate, \
    has_required_request_params, non_empty_int, log_304, \
    get_user_by_email, set_date_from_int


class SampleResource(BaseResource):
    fields = {
        'theme.name': fields.String,
        'user.email': fields.String,
        'user.first_name': fields.String,
        'user.last_name': fields.String,
        'animal_species': fields.String,
        'sample_type': fields.String,
        'sample_description': fields.String,
        'location_collected': fields.String,
        'project': fields.String,
        'project_owner': fields.String,
        'retention_date': fields.DateTime,
        'barcode': fields.String,
        'analysis': fields.String,
        'temperature': fields.String,
        'amount': fields.Integer,
        'quantity.id': fields.String,
        'secLevel.code': fields.String,
        'secLevel.name': fields.String,
        'code': fields.String,
        'created_at': fields.String,
        'updated_at': fields.String,
        'box.label': fields.String,
        'box.tray.number': fields.Integer,
        'box.tray.rack.number': fields.Integer,
        'box.tray.rack.chamber.type': fields.String,
        'box.tray.rack.chamber.freezer.number': fields.Integer,
        'box.tray.rack.chamber.freezer.lab.name': fields.String,
        'box.tray.rack.chamber.freezer.lab.room': fields.Integer

    }

    def get(self):
        if request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
            sample = SampleResource.get_sample(code)
            if sample is None:
                return BaseResource.send_json_message("Sample not found", 404)
            data = marshal(sample, self.fields)
            return BaseResource.send_json_message(data, 200)

        else:
            samples = Sample.query.all()
            if samples is None:
                return BaseResource.send_json_message("Samples not found", 404)
            data = marshal(samples, self.fields)
            return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = SampleResource.sample_args()
        code = format_and_lower_str(args[16])
        theme = ThemeResource.get_theme(args[0]).id
        user = get_user_by_email(args[1]).id
        box = BoxResource.get_box(args[2]).id
        qt = QuantityTypeResource.get_quantity_type(args[14]).id
        sl = SecurityLevelResource.get_security_level(args[15]).id

        if not Sample.sample_exists(code):
            try:
                sample = Sample(theme_id=theme, user_id=user, box_id=box, animal_species=args[3],
                                sample_type=args[4], sample_description=args[5], location_collected=args[6],
                                project=args[7], project_owner=args[8], retention_date=args[9], barcode=args[10],
                                analysis=args[11], temperature=args[12], amount=args[13], quantity_type=qt,
                                security_level=sl, code=code)

                BaseModel.db.session.add(sample)
                BaseModel.db.session.commit()
                log_create(sample)
                return BaseResource.send_json_message("Sample successfully created", 201)
            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding sample", 500)
        log_duplicate(Sample.query.filter(Sample.code == code).first())
        return BaseResource.send_json_message("Sample already exists", 409)

    @jwt_required
    @is_sample_owner
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        sample = SampleResource.get_sample(code)

        if sample is not None:
            args = SampleResource.sample_args()
            if args[0] != sample.theme_id or args[1] != sample.user_id or \
                    args[2] != sample.box_id or args[3] != sample.animal_species or \
                    args[4] != sample.sample_type or args[5] != sample.sample_description \
                    or args[6] != sample.location_collected or args[7] != sample.project \
                    or args[8] != sample.project_owner or \
                    args[9] != sample.retention_date \
                    or args[10] != sample.barcode or args[11] != sample.analysis or args[12] != sample.temperature \
                    or args[13] != sample.amount or args[14] != sample.quantity_type or args[
                15] != sample.security_level or args[16] != sample.code:
                try:
                    code = format_and_lower_str(args[16])
                    theme = ThemeResource.get_theme(args[0]).id
                    user = get_user_by_email(args[1]).id
                    box = BoxResource.get_box(args[2]).id
                    qt = QuantityTypeResource.get_quantity_type(args[14]).id
                    sl = SecurityLevelResource.get_security_level(args[15]).id

                    old_info = str(sample)
                    sample.theme_id = theme
                    sample.user_id = user
                    sample.box_id = box
                    sample.animal_species = args[3]
                    sample.sample_type = args[4]
                    sample.sample_description = args[5]
                    sample.location_collected = args[6]
                    sample.project = args[7]
                    sample.project_owner = args[8]
                    sample.retention_date = args[9]
                    sample.barcode = args[10]
                    sample.analysis = args[11]
                    sample.temperature = args[12]
                    sample.amount = args[13]
                    sample.quantity_type = qt
                    sample.security_level = sl
                    sample.code = code

                    sample.updated_at = datetime.now()
                    BaseModel.db.session.commit()
                    log_update(old_info, sample)
                    return BaseResource.send_json_message("Sample successfully updated", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding sample. Another sample has that name or "
                                                          "code", 500)
            log_304(sample)
            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("Sample not found", 404)

    @jwt_required
    @is_sample_owner
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
        sample = SampleResource.get_sample(code)

        if not sample:
            return BaseResource.send_json_message("Sample not found", 404)

        else:
            BaseModel.db.session.delete(sample)
            BaseModel.db.session.commit()
            current_app.logger.info("{0} deleted {1}".format(get_jwt_identity(), sample.user_id))
            return BaseResource.send_json_message("Sample deleted", 200)

    @staticmethod
    def sample_args():
        parser = reqparse.RequestParser()
        parser.add_argument('theme', required=True)
        parser.add_argument('user', required=False, type=non_empty_int)
        parser.add_argument('box', required=False)
        parser.add_argument('animal_species', required=False)
        parser.add_argument('sample_type', required=False)
        parser.add_argument('sample_description', required=False)
        parser.add_argument('location_collected', required=False)
        parser.add_argument('project', required=False)
        parser.add_argument('project_owner', required=True)
        parser.add_argument('retention_period', required=True)
        parser.add_argument('barcode', required=True)
        parser.add_argument('analysis', required=True)
        parser.add_argument('temperature', required=True)
        parser.add_argument('amount', required=True)
        parser.add_argument('quantity_type', required=True)
        parser.add_argument('security_level', required=True)
        parser.add_argument('code', required=True)

        args = parser.parse_args()

        theme_id = args['theme']
        user_id = args['user']
        box_id = args['box']
        animal_species = args['animal_species']
        sample_type = args['sample_type']
        sample_description = args['sample_description']
        location_collected = args['location_collected']
        project = args['project']
        project_owner = args['project_owner']
        retention_date = set_date_from_int(int(args['retention_period']))
        print("Args for retention passed: " + str(args['retention_period']) + " of type: "
              + str(type(args['retention_period'])))
        print("Retention period is: " + str(retention_date) + " of type " + str(type(retention_date)))
        barcode = args['barcode']
        analysis = args['analysis']
        temperature = float(args['temperature'])
        amount = int(args['amount'])
        quantity_type = str(args['quantity_type'])
        security_level = format_and_lower_str(args['security_level'])
        code = format_and_lower_str(args['code'])

        return [
            theme_id, user_id, box_id, animal_species, sample_type, sample_description, location_collected,
            project, project_owner, retention_date, barcode, analysis, temperature, amount, quantity_type,
            security_level, code
        ]

    @staticmethod
    def get_sample(sample_code):
        return BaseModel.db.session.query(Sample).filter_by(code=sample_code).first()
