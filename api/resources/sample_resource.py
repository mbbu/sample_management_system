from flask import current_app
from flask_restful import fields, marshal, reqparse

from api.models.database import BaseModel
from api.models.sample import Sample
from api.resources.base_resource import BaseResource


class SampleResource(BaseResource):
    fields = {
        'theme_id': fields.Integer,
        'user_id': fields.Integer,
        'box_id': fields.Integer,
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
        'amount': fields.Integer
    }

    def get(self):
        samples = Sample.query.all()
        data = marshal(samples, self.fields)
        # return output_json(data, 200)
        return BaseResource.send_json_message(data, 200)

    def post(self):
        args = SampleResource.sample_args()
        sample = Sample(theme_id=args[0], user_id=args[1], box_id=args[2], animal_species=args[3],
                        sample_type=args[4], sample_description=args[5], location_collected=args[6],
                        project=args[7], project_owner=args[8], retention_period=args[9], barcode=args[10],
                        analysis=args[11], temperature=args[12],
                        amount=args[13])

        BaseModel.db.session.add(sample)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Sample created", 201)

    def put(self, id):
        sample = SampleResource.get_sample(id)
        args = SampleResource.sample_args()

        if sample is not None:
            if args[0] != sample.theme_id or args[1] != sample.user_id or \
                    args[2] != sample.box_id or args[3] != sample.animal_species or \
                    args[4] != sample.sample_type or args[5] != sample.sample_description \
                    or args[6] != sample.location_collected or args[7] != sample.project \
                    or args[8] != sample.project_owner or args[9] != sample.retention_period \
                    or args[10] != sample.barcode or args[11] != sample.analysis or args[12] != sample.temperature \
                    or args[13] != sample.amount:
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

                    BaseModel.db.session.commit()
                    return BaseResource.send_json_message("Updated the Sample", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding sample. Another sample has that name or "
                                                          "code", 500)

            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("Sample not found", 404)

    def delete(self, id):
        sample = SampleResource.get_sample(id)

        if not sample:
            return BaseResource.send_json_message("Sample not found", 404)

        BaseModel.db.session.delete(sample)
        BaseModel.db.session.commit()

        return BaseResource.send_json_message("Sample Successfully deleted", 200)

    @staticmethod
    def sample_args():
        parser = reqparse.RequestParser()
        parser.add_argument('theme_id', required=False)
        parser.add_argument('user_id', required=False)
        parser.add_argument('box_id', required=False)
        parser.add_argument('animal_species', required=True)
        parser.add_argument('sample_type', required=True)
        parser.add_argument('sample_description', required=True)
        parser.add_argument('location_collected', required=True)
        parser.add_argument('project', required=True)
        parser.add_argument('project_owner', required=True)
        parser.add_argument('retention_period', required=True)
        parser.add_argument('barcode', required=True)
        parser.add_argument('analysis', required=True)
        parser.add_argument('temperature', required=True)
        parser.add_argument('amount', required=True)

        args = parser.parse_args()

        theme_id = int(args['theme_id'])
        user_id = int(args['user_id'])
        box_id = int(args['box_id'])
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

        return [
            theme_id, user_id, box_id, animal_species, sample_type, sample_description, location_collected,
            project, project_owner, retention_period, barcode, analysis, temperature, amount
        ]

    @staticmethod
    def get_sample(sample_id):
        return BaseModel.db.session.query(Sample).get(sample_id)
