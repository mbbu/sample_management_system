from datetime import timedelta, datetime

from flask import current_app, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import fields, marshal, reqparse

from api.constants import DATE_TIME_NONE
from api.models.database import BaseModel
from api.models.sample import Sample
from api.resources.base_resource import BaseResource
from api.utils import format_and_lower_str, log_create, log_update, log_duplicate, \
    has_required_request_params, export_all_records, log_export_from_redcap, format_str_to_date, non_empty_int, log_304

samples_page = Blueprint('samples_bp', __name__, template_folder='templates')


class SampleResource(BaseResource):
    fields = {
        'theme.name': fields.String,
        'user.email': fields.String,
        'user.first_name': fields.String,
        'user.last_name': fields.String,
        'box.label': fields.String,
        'animal_species': fields.String,
        'sample_type': fields.String,
        'sample_description': fields.String,
        'location_collected': fields.String,
        'project': fields.String,
        'project_owner': fields.String,
        'retention_period': fields.Integer,
        'barcode': fields.String,
        'analysis': fields.String,
        'temperature': fields.String,  # todo: check temp return i.e. float
        'amount': fields.Integer,
        'quantity.id': fields.String,
        'security_level': fields.Integer,
        'code': fields.String
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

        if not Sample.sample_exists(code):
            try:
                sample = Sample(theme_id=args[0], user_id=args[1], box_id=args[2], animal_species=args[3],
                                sample_type=args[4], sample_description=args[5], location_collected=args[6],
                                project=args[7], project_owner=args[8], retention_period=args[9], barcode=args[10],
                                analysis=args[11], temperature=args[12], amount=args[13], quantity_type=args[14],
                                security_level=args[15], code=code)

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
                    or args[8] != sample.project_owner or args[9] != sample.retention_period \
                    or args[10] != sample.barcode or args[11] != sample.analysis or args[12] != sample.temperature \
                    or args[13] != sample.amount or args[14] != sample.quantity_type or args[
                15] != sample.security_level or args[16] != sample.code:
                try:
                    old_info = str(sample)
                    sample.theme_id = args[0]
                    sample.user_id = args[1]
                    sample.box_id = args[2]
                    sample.animal_species = args[3]
                    sample.sample_type = args[4]
                    sample.sample_description = args[5]
                    sample.location_collected = args[6]
                    sample.project = args[7]
                    sample.project_owner = args[8]
                    sample.retention_period = args[9]
                    sample.barcode = args[10]
                    sample.analysis = args[11]
                    sample.temperature = args[12]
                    sample.amount = args[13]
                    sample.quantity_type = args[14]
                    sample.security_level = args[15]
                    sample.code = args[16]

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
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
        sample = SampleResource.get_sample(code)

        if not sample:
            return BaseResource.send_json_message("Sample not found", 404)

        else:
            sample.is_deleted = True
            sample.deleted_at = datetime.now()
            sample.deleted_by = get_jwt_identity()
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

        theme_id = int(args['theme'])
        user_id = int(args['user'])
        box_id = args['box']
        animal_species = args['animal_species']
        sample_type = args['sample_type']
        sample_description = args['sample_description']
        location_collected = args['location_collected']
        project = args['project']
        project_owner = args['project_owner']
        retention_period = int(args['retention_period'])
        barcode = args['barcode']
        analysis = args['analysis']
        temperature = float(args['temperature'])
        amount = int(args['amount'])
        quantity_type = str(args['quantity_type'])
        security_level = format_and_lower_str(args['security_level'])
        code = format_and_lower_str(args['code'])

        return [
            theme_id, user_id, box_id, animal_species, sample_type, sample_description, location_collected,
            project, project_owner, retention_period, barcode, analysis, temperature, amount, quantity_type,
            security_level, code
        ]

    @staticmethod
    def get_sample(sample_code):
        return BaseModel.db.session.query(Sample).filter_by(code=sample_code).first()


class SaveSampleFromREDCap(BaseResource):
    @jwt_required
    def post(self):
        # get any filters for data export e.g. date, record_id ...
        parser = reqparse.RequestParser()
        parser.add_argument('from', required=False)
        parser.add_argument('to', required=False)
        parser.add_argument('record_id', required=False)

        args = parser.parse_args()

        if args['from'] or args['to'] or args['record_id'] is None:
            start_date = None
            end_date = None
            record_id = None
        else:
            start_date = format_str_to_date(args['from'] + str(' 00:00'))
            end_date = format_str_to_date(args['to'] + str(' 00:00'))
            record_id = args['record_id']

        sample_records = export_all_records()
        if sample_records == 404:
            # todo: mail admin on redcap error
            return BaseResource.send_json_message("Redcap error. Admin contacted.", 404)
        else:
            if (start_date or end_date or record_id) is None:
                # save all the samples to the db
                SaveSampleFromREDCap.save_all_samples(sample_records)
            else:
                # save samples according to the filters passed
                SaveSampleFromREDCap.save_samples_filtered_by_date(sample_records, start_date, end_date)

    @staticmethod
    def save_all_samples(sample_records):
        for sample in sample_records:
            user = int(sample['users'].strip() or 0) or None
            animal_species = sample['source_sample']
            _type = sample['sample_type']
            description = sample['sa_description']
            location = sample['loc_sample']
            owner = sample['pi']
            amount = int(sample['number_samples_collected'].strip() or 0) or None
            box = int(sample['box_number'].strip() or 0) or None
            theme = int(sample['theme'].strip() or 0) or None
            security_level = int(sample['risk_level'].strip() or 0) or None
            record_id = sample['identifier_sample']

            if not Sample.sample_exists(record_id):
                sample = Sample(code=record_id, theme_id=theme, user_id=user, box_id=box, animal_species=animal_species,
                                sample_type=_type, sample_description=description, location_collected=location,
                                project_owner=owner, amount=amount, security_level=security_level)

                BaseModel.db.session.add(sample)
                BaseModel.db.session.commit()
                log_export_from_redcap(sample)
            log_duplicate(Sample.query.filter(Sample.code == record_id).first())
            return BaseResource.send_json_message("Sample already exists", 409)
        return BaseResource.send_json_message("Samples successfully fetched and saved", 201)

    @staticmethod
    def save_samples_filtered_by_date(sample_records, start_date, end_date):
        days_count = end_date - start_date

        for day in range(days_count.days + 1):
            day = start_date + timedelta(days=day)
            print(day)

            for sample in sample_records:
                _date = format_str_to_date(sample['date'] or DATE_TIME_NONE)

                if day == _date:
                    user = int(sample['users'].strip() or 0) or None
                    animal_species = sample['source_sample']
                    _type = sample['sample_type']
                    description = sample['sa_description']
                    location = sample['loc_sample']
                    owner = sample['pi']
                    amount = int(sample['number_samples_collected'].strip() or 0) or None
                    box = int(sample['box_number'].strip() or 0) or None
                    theme = int(sample['theme'].strip() or 0) or None
                    security_level = int(sample['risk_level'].strip() or 0) or None
                    record_id = sample['identifier_sample']

                    if not Sample.sample_exists(record_id):
                        sample = Sample(code=record_id, theme_id=theme, user_id=user, box_id=box,
                                        animal_species=animal_species, sample_type=_type,
                                        sample_description=description,
                                        location_collected=location, project_owner=owner, amount=amount,
                                        security_level=security_level)

                        BaseModel.db.session.add(sample)
                        BaseModel.db.session.commit()
                        log_export_from_redcap(sample)
                    log_duplicate(Sample.query.filter(Sample.code == record_id).first())
                    return BaseResource.send_json_message("Sample already exists", 409)
        return BaseResource.send_json_message(
            "Samples from date {0} to date {1} saved".format(start_date, end_date), 201)
