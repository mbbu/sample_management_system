from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.sample import Sample
from api.resources.base_resource import BaseResource
from api.utils import format_and_lower_str, log_create, log_update, log_delete, log_duplicate


class SampleResource(BaseResource):
    fields = {
        'theme.name': fields.String,
        'user.email': fields.Integer,
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
        'temperature': fields.String,
        'amount': fields.Integer,
        'quantity.id': fields.String,
        'code': fields.String
    }

    def get(self):
        if request.headers.get('label') is not None:
            code = format_and_lower_str(request.headers['code'])()
            sample = SampleResource.get_sample(code)
            data = marshal(sample, self.fields)
            return BaseResource.send_json_message(data, 200)
        else:
            samples = Sample.query.all()
            data = marshal(samples, self.fields)
            return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = SampleResource.sample_args()
        code = format_and_lower_str(args[14])()

        if not Sample.sample_exists(code):
            try:
                sample = Sample(theme_id=args[0], user_id=args[1], box_id=args[2], animal_species=args[3],
                                sample_type=args[4], sample_description=args[5], location_collected=args[6],
                                project=args[7], project_owner=args[8], retention_period=args[9], barcode=args[10],
                                analysis=args[11], temperature=args[12], amount=args[13], code=args[14],
                                quantity_type=args[15])

                BaseModel.db.session.add(sample)
                BaseModel.db.session.commit()
                log_create(sample)
                return BaseResource.send_json_message("Sample created", 201)
            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding sample", 500)
        log_duplicate(Sample.query.filter(Sample.code == code).first())
        return BaseResource.send_json_message("Sample already exists", 500)

    @jwt_required
    def put(self):
        code = format_and_lower_str(request.headers['code'])()
        sample = SampleResource.get_sample(code)
        args = SampleResource.sample_args()

        if sample is not None:
            if args[0] != sample.theme_id or args[1] != sample.user_id or \
                    args[2] != sample.box_id or args[3] != sample.animal_species or \
                    args[4] != sample.sample_type or args[5] != sample.sample_description \
                    or args[6] != sample.location_collected or args[7] != sample.project \
                    or args[8] != sample.project_owner or args[9] != sample.retention_period \
                    or args[10] != sample.barcode or args[11] != sample.analysis or args[12] != sample.temperature \
                    or args[13] != sample.amount or args[14] != sample.code or args[15 != sample.quantity_type]:
                try:
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
                    sample.code = args[14]
                    sample.quantity_type = args[15]

                    BaseModel.db.session.commit()
                    log_update(sample, sample)
                    return BaseResource.send_json_message("Updated the Sample", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding sample. Another sample has that name or "
                                                          "code", 500)

            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("Sample not found", 404)

    @jwt_required
    def delete(self):
        code = format_and_lower_str(request.headers['code'])()
        sample = SampleResource.get_sample(code)

        if not sample:
            return BaseResource.send_json_message("Sample not found", 404)

        BaseModel.db.session.delete(sample)
        BaseModel.db.session.commit()
        log_delete(sample)
        return BaseResource.send_json_message("Sample Successfully deleted", 200)

    @staticmethod
    def sample_args():
        parser = reqparse.RequestParser()
        parser.add_argument('theme', required=False)
        parser.add_argument('user', required=False)
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
        parser.add_argument('code', required=True)

        args = parser.parse_args()

        theme_id = int(args['theme'])
        user_id = int(args['user'])
        box_id = int(args['box'])
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
        code = format_and_lower_str(args['code'])()

        return [
            theme_id, user_id, box_id, animal_species, sample_type, sample_description, location_collected,
            project, project_owner, retention_period, barcode, analysis, temperature, amount, code, quantity_type
        ]

    @staticmethod
    def get_sample(sample_code):
        return BaseModel.db.session.query(Sample).filter_by(code=sample_code).first()
