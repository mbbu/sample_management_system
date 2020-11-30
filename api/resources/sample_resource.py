import json

from datetime import datetime

from flask import current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import fields, marshal, reqparse

from api.constants import SAMPLE_IN_LAB
from api.models.database import BaseModel
from api.models.sample import Sample
from api.resources.base_resource import BaseResource
from api.resources.bio_hazard_level_resource import BioHazardLevelResource
from api.resources.decorators.user_role_decorators import is_sample_owner
from api.resources.project_resource import ProjectResource
from api.resources.quantity_type_resource import QuantityTypeResource
from api.resources.slot_resource import SlotResource
from api.resources.theme_resource import ThemeResource
from api.utils import format_and_lower_str, log_create, log_update, log_duplicate, \
    has_required_request_params, non_empty_int, log_304, set_date_from_int, get_any_user_by_email, get_query_params, \
    fake


class SampleResource(BaseResource):
    fields = {
        'status': fields.String,
        'theme.name': fields.String,
        # user is the sample owner
        'user.email': fields.String,
        'user.first_name': fields.String,
        'user.last_name': fields.String,
        'animal_species': fields.String,
        'sample_type': fields.String,
        'sample_description': fields.String,
        'location_collected': fields.String,
        'project.name': fields.String,
        'project.lead.first_name': fields.String,
        'project.lead.last_name': fields.String,
        'retention_date': fields.DateTime,
        'barcode': fields.String,
        'analysis': fields.String,
        'temperature': fields.String,
        'amount': fields.Integer,
        'quantity.id': fields.String,
        'bioHazardLevel.code': fields.String,
        'bioHazardLevel.name': fields.String,
        'code': fields.String,
        'created_at': fields.String,
        'updated_at': fields.String,
        'slot.position': fields.String,
        'slot.box.label': fields.String,
        'slot.box.tray.number': fields.String,
        'slot.box.tray.rack.number': fields.String,
        'slot.box.tray.rack.chamber.type': fields.String,
        'slot.box.tray.rack.chamber.freezer.number': fields.String,
        'slot.box.tray.rack.chamber.freezer.lab.name': fields.String,
        'slot.box.tray.rack.chamber.freezer.lab.room': fields.String

    }

    def get(self):
        query_strings = get_query_params()
        if query_strings is not None:
            for query_string in query_strings:
                query, total = Sample.search(query_string, 1, 15)
                samples = query.all()

                data = marshal(samples, self.fields)
                return BaseResource.send_json_message(data, 200)

        elif request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
            sample = SampleResource.get_sample(code)
            if sample is None:
                return BaseResource.send_json_message("Sample not found", 404)
            data = marshal(sample, self.fields)
            return BaseResource.send_json_message(data, 200)

        else:
            samples = SampleResource.get_samples()
            if samples is None:
                return BaseResource.send_json_message("Samples not found", 404)
            data = marshal(samples, self.fields)
            return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = SampleResource.sample_args()
        slots = json.loads(args['slots'])

        # register multiple samples
        for i in range(len(slots)):
            code = fake.ean(length=8)
            barcode = fake.ean(length=13)
            slot = SlotResource.get_slot(slots[i])

            if not Sample.sample_exists(code):
                try:
                    sample = Sample()

                    SampleResource.save_sample(sample, args, barcode, slot, code)
                    slot.available = False  # update that the slot is no longer available

                    BaseModel.db.session.add(sample)
                    log_create(sample)
                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding sample", 500)
            else:
                log_duplicate(Sample.query.filter(Sample.code == code).first())
                return BaseResource.send_json_message("Sample already exists", 409)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Registered " + str(len(slots)) + " samples.", 201)

    @jwt_required
    @is_sample_owner
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        sample = SampleResource.get_sample(code)

        if sample is not None:
            args = SampleResource.sample_args()

            if args['code'] != sample.code or args['theme'] != sample.theme_id \
                    or args['user'] != sample.user_id or args['slot'] != sample.slot_id \
                    or args['species'] != sample.animal_species or args['type'] != sample.sample_type \
                    or args['project'] != sample.project or args['project_owner'] != sample.project_owner \
                    or args['desc'] != sample.sample_description or args['location'] != sample.location_collected \
                    or args['amount'] != sample.amount or args['quantity_type'] != sample.quantity_type \
                    or args['barcode'] != sample.barcode or args['analysis'] != sample.analysis \
                    or args['bio_hazard_level'] != sample.bio_hazard_level \
                    or args['retention_date'] != sample.retention_date \
                    or args['temperature'] != sample.temperature:

                try:
                    code = format_and_lower_str(args['code'])
                    user = get_any_user_by_email(args['user']).id
                    slot = SlotResource.get_slot(args['slot']).id
                    theme = ThemeResource.get_theme(args['theme']).id
                    qt = QuantityTypeResource.get_quantity_type(args['quantity_type']).id
                    bhl = BioHazardLevelResource.get_bio_hazard_level(args['bio_hazard_level']).id

                    old_info = str(sample)

                    sample.code = code
                    sample.slot_id = slot
                    sample.user_id = user
                    sample.theme_id = theme
                    sample.quantity_type = qt
                    sample.bio_hazard_level = bhl
                    sample.status = SAMPLE_IN_LAB
                    sample.amount = args['amount']
                    sample.barcode = args['barcode']
                    sample.project = args['project']
                    sample.sample_type = args['type']
                    sample.analysis = args['analysis']
                    sample.project_owner = args['project']
                    sample.animal_species = args['species']
                    sample.sample_description = args['desc']
                    sample.temperature = args['temperature']
                    sample.location_collected = args['location']
                    sample.retention_date = args['retention_date']

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
        parser.add_argument('slots', required=False)
        parser.add_argument('amount', required=True)
        parser.add_argument('project', required=False)
        parser.add_argument('analysis', required=True)
        parser.add_argument('temperature', required=True)
        parser.add_argument('sample_type', required=False)
        parser.add_argument('project_owner', required=True)
        parser.add_argument('quantity_type', required=True)
        parser.add_argument('animal_species', required=False)
        parser.add_argument('retention_period', required=True)
        parser.add_argument('bio_hazard_level', required=True)
        parser.add_argument('sample_description', required=False)
        parser.add_argument('location_collected', required=False)
        parser.add_argument('user', required=False, type=non_empty_int)  # user is the sample owner

        args = parser.parse_args()
        return {
            'user': args['user'],
            'slots': args['slots'],
            'theme': args['theme'],
            'project': args['project'],
            'type': args['sample_type'],
            'analysis': args['analysis'],
            'amount': int(args['amount']),
            'species': args['animal_species'],
            'desc': args['sample_description'],
            'location': args['location_collected'],
            'project_owner': args['project_owner'],
            'temperature': float(args['temperature']),
            'quantity_type': str(args['quantity_type']),
            'retention_date': set_date_from_int(int(args['retention_period'])),
            'bio_hazard_level': format_and_lower_str(args['bio_hazard_level']),
        }

    @staticmethod
    def get_sample(sample_code):
        return BaseModel.db.session.query(Sample).filter_by(code=sample_code).first()

    @staticmethod
    def get_samples():
        return BaseModel.db.session.query(Sample).all()

    @staticmethod
    def save_sample(sample, args, barcode, slot, code):

        theme = ThemeResource.get_theme(args['theme']).id
        user = get_any_user_by_email(args['user']).id
        qt = QuantityTypeResource.get_quantity_type(args['quantity_type']).id
        bhl = BioHazardLevelResource.get_bio_hazard_level(args['bio_hazard_level']).id
        project = ProjectResource.get_project(args['project']).id

        sample.theme_id, sample.user_id, sample.slot_id = theme, user, slot.id
        sample.animal_species, sample.sample_type = args['species'], args['type']
        sample.sample_description, sample.location_collected = args['desc'], args['location']
        sample.barcode, sample.project_id = barcode, project
        sample.temperature, sample.amount, sample.quantity_type = args['temperature'], args['amount'], qt
        sample.retention_date, sample.analysis = args['retention_date'], args['analysis']
        sample.bio_hazard_level, sample.code, sample.status = bhl, code, SAMPLE_IN_LAB

        return sample
