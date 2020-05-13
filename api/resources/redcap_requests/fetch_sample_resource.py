from datetime import timedelta

from flask_jwt_extended import jwt_required
from flask_restful import reqparse

from api import BaseResource, BaseModel
from api.constants import DATE_TIME_NONE
from api.models import Sample
from api.utils import format_str_to_date, export_all_records, log_export_from_redcap, log_duplicate


class SaveSampleFromREDCap(BaseResource):
    @jwt_required
    def post(self):
        print("Call of post")
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
        print(sample_records)

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
