from datetime import timedelta

import requests
from flask import request, current_app
from flask_jwt_extended import jwt_required
from flask_restful import reqparse

from api import BaseResource, BaseModel, BaseConfig
from api.constants import DATE_TIME_NONE, REDCAP_URI
from api.models import Sample
from api.resources.box_resource import BoxResource
from api.resources.theme_resource import ThemeResource
from api.utils import format_str_to_date, log_export_from_redcap, log_duplicate, get_user_by_email


class SaveSampleFromREDCap(BaseResource):
    @jwt_required
    def post(self):
        print("Call of post")

        parser = reqparse.RequestParser()
        parser.add_argument('from', required=False)
        parser.add_argument('to', required=False)
        parser.add_argument('project', required=False)

        args = parser.parse_args()

        # if args['from'] or args['to'] or args['project'] is None:
        #     start_date = None
        #     end_date = None
        #     project = None
        # else:

        # todo: resolve issue with format of datetime
        # start_date = format_str_to_date(args['from'] + str(' 00:00'))
        # end_date = format_str_to_date(args['to'] + str(' 00:00'))
        # project = args['project']

        sample_records = export_all_records()
        print(sample_records)

        if sample_records == 500:
            # todo: mail admin on redcap error
            return BaseResource.send_json_message("Redcap error. Admin contacted.", 500)
        elif not sample_records:
            return BaseResource.send_json_message("No sample records found", 404)
        else:
            # if (start_date or end_date or project) is None:
            # save all the samples to the db
            SaveSampleFromREDCap.save_all_samples(sample_records)
            # else:
            # save samples according to the filters passed
            # SaveSampleFromREDCap.save_samples_filtered_by_date(sample_records, start_date, end_date)

    @staticmethod
    def save_all_samples(sample_records):
        for sample_record in sample_records:
            """
                data returned from redcap:
                    {
                    //"record_id":"1",
                    "name":"andrewespira", ? user_id
                    "mail":"aespira@icipe.org", ? user_id
                    "theme":"1", -> theme_id how to know theme 
                    "project":"IBCARP", -> project
                    ??"sample_type":"1", -> sample_type how to know sample types
                    "sample_id":"bm01_c2_01", -> ? code
                    //"lab":"1", -> ?
                    //"room_id":"ml-05", -> ?
                    //"freezer_id":"mbbu-005", -> ?
                    "box_id":"cd-07", -> box_id
                    //"rack_id":"4",
                    ??"amount_taken":"7", -> amount
                    "date_return":"2020-05-30 11:55",
                    //"sample_request_form_complete":"2",
                    $"project_name":"ibcarp",
                    //"project_id":"008",
                    "staff_in_charge":"andre espira", -> ? user_id
                    "collection_type":"gf", -> ? description
                    "longitude":"36.8968905","lat":"-1.2215215000000001", -> location_collected
                    "label_sample":"cd",
                    ??"sample_type_collected":"blood", -> sample_type
                    ??"amount":"400", -> amount
                    "condition":"safe", -> ? security_level
                    "level":"7",
                    }         
            """

            # use python ternary operator to avoid errors

            user = None if AttributeError else get_user_by_email(sample_record['mail']).id
            # todo: if user is not assigned, then assign it either to admin or theme admin
            sample_type = sample_record['sample_type_collected']
            project = sample_record['project']
            box = None if AttributeError else BoxResource.get_box(sample_record['box_id']).id
            theme = None if AttributeError else ThemeResource.get_theme(sample_record['theme']).id
            code = sample_record['sample_id']
            amount = sample_record['amount']
            location_collected = {'lat': sample_record['lat'], 'long': sample_record['longitude']}

            print(user)
            print(sample_type)
            print(project)
            print(box)
            print(theme)
            print(code)
            print(amount)
            print(location_collected)
            print(type(location_collected))


        #     # user = int(sample['users'].strip() or 0) or None
        #     animal_species = sample['source_sample']
        #     _type = sample['sample_type']
        #     description = sample['sa_description']
        #     location = sample['loc_sample']
        #     owner = sample['pi']
        #     amount = int(sample['number_samples_collected'].strip() or 0) or None
        #     box = int(sample['box_number'].strip() or 0) or None
        #     theme = int(sample['theme'].strip() or 0) or None
        #     security_level = int(sample['risk_level'].strip() or 0) or None
        #     record_id = sample['identifier_sample']
        #
        #     if not Sample.sample_exists(record_id):
        #         sample = Sample(code=record_id, theme_id=theme, user_id=user, box_id=box, animal_species=animal_species,
        #                         sample_type=_type, sample_description=description, location_collected=location,
        #                         project_owner=owner, amount=amount, security_level=security_level)
        #
        #         BaseModel.db.session.add(sample)
        #         BaseModel.db.session.commit()
        #         log_export_from_redcap(sample)
        #     log_duplicate(Sample.query.filter(Sample.code == record_id).first())
        #     return BaseResource.send_json_message("Sample already exists", 409)
        # return BaseResource.send_json_message("Samples successfully fetched and saved", 201)

    # @staticmethod
    # def save_samples_filtered_by_date(sample_records, start_date, end_date):
    #     days_count = end_date - start_date
    #
    #     for day in range(days_count.days + 1):
    #         day = start_date + timedelta(days=day)
    #         print(day)
    #
    #         for sample in sample_records:
    #             _date = format_str_to_date(sample['date'] or DATE_TIME_NONE)
    #
    #             if day == _date:
    #                 user = int(sample['users'].strip() or 0) or None
    #                 animal_species = sample['source_sample']
    #                 _type = sample['sample_type']
    #                 description = sample['sa_description']
    #                 location = sample['loc_sample']
    #                 owner = sample['pi']
    #                 amount = int(sample['number_samples_collected'].strip() or 0) or None
    #                 box = int(sample['box_number'].strip() or 0) or None
    #                 theme = int(sample['theme'].strip() or 0) or None
    #                 security_level = int(sample['risk_level'].strip() or 0) or None
    #                 record_id = sample['identifier_sample']
    #
    #                 if not Sample.sample_exists(record_id):
    #                     sample = Sample(code=record_id, theme_id=theme, user_id=user, box_id=box,
    #                                     animal_species=animal_species, sample_type=_type,
    #                                     sample_description=description,
    #                                     location_collected=location, project_owner=owner, amount=amount,
    #                                     security_level=security_level)
    #
    #                     BaseModel.db.session.add(sample)
    #                     BaseModel.db.session.commit()
    #                     log_export_from_redcap(sample)
    #                 log_duplicate(Sample.query.filter(Sample.code == record_id).first())
    #                 return BaseResource.send_json_message("Sample already exists", 409)
    #     return BaseResource.send_json_message(
    #         "Samples from date {0} to date {1} saved".format(start_date, end_date), 201)
    #


"""
    REDCap API functions
"""


# fetch all records
def export_all_records():
    # print("Redcap contact made")
    token = request.headers.get('token')
    data = {
        'token': BaseConfig.REDCap_API_TOKEN or token,
        'content': 'record',
        'format': 'json',
        'returnFormat': 'json'
    }

    try:
        response = requests.post(REDCAP_URI, data)
        # print(response)
        # print(response.status_code)
        # print(response.json())
        return response.json()

    except Exception as e:
        current_app.logger.error(e)
        return 500
