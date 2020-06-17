import requests
from flask import request, current_app
from flask_jwt_extended import jwt_required
from flask_restful import reqparse

from api import BaseResource, BaseModel, BaseConfig
from api.constants import REDCAP_URI
from api.models import Sample
from api.resources.box_resource import BoxResource
from api.resources.theme_resource import ThemeResource
from api.utils import log_export_from_redcap, log_duplicate, get_user_by_email


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
            return SaveSampleFromREDCap.save_all_samples(sample_records)
            # else:
            # save samples according to the filters passed
            # SaveSampleFromREDCap.save_samples_filtered_by_date(sample_records, start_date, end_date)

    @staticmethod
    def save_all_samples(sample_records):
        for sample_record in sample_records:
            """
                data returned from redcap:
                    {
                    "name":"andrewespira", ? user_id
                    "mail":"aespira@icipe.org", ? user_id
                    "theme":"1", -> theme_id how to know theme 
                    "project":"IBCARP", -> project
                    ??"sample_type":"1", -> sample_type how to know sample types
                    "sample_id":"bm01_c2_01", -> ? code
                    "box_id":"cd-07", -> box_id
                    "date_return":"2020-05-30 11:55",
                    $"project_name":"ibcarp",
                    "staff_in_charge":"andre espira", -> ? user_id
                    "collection_type":"gf", -> ? description
                    "longitude":"36.8968905","lat":"-1.2215215000000001", -> location_collected
                    "label_sample":"cd",
                    ??"sample_type_collected":"blood", -> sample_type
                    ??"amount":"400", -> amount
                    "condition":"safe", -> ? security_level
                    "level":"7",
                    
                    
                    //"record_id":"1",
                    //"rack_id":"4",
                    //"sample_request_form_complete":"2",
                    //"lab":"1", -> ?
                    //"project_id":"008",
                    //"room_id":"ml-05", -> ?
                    //"freezer_id":"mbbu-005", -> ?
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
            amount = None if ValueError else int(sample_record['amount'])
            location = {'lat': sample_record['lat'], 'long': sample_record['longitude']}
            owner = sample_record['staff_in_charge']

            # todo: fields-not-found
            '''
                 animal_species
                 sample_description
                 security_level
                 QT
                 SL
                 Temp
                 Retention
            '''
            if not Sample.sample_exists(code):
                print("success if block")
                sample = Sample(code=code, theme_id=theme, user_id=user, box_id=box,
                                sample_type=sample_type, location_collected=location,
                                project_owner=owner, amount=amount)

                BaseModel.db.session.add(sample)
                BaseModel.db.session.commit()
                log_export_from_redcap(sample)
                return BaseResource.send_json_message("Samples successfully fetched and saved", 201)
            log_duplicate(Sample.query.filter(Sample.code == code).first())
            # if an existing sample is encountered, do not return before finishing on other samples,
            # instead move control back to the for loop
            continue
        return BaseResource.send_json_message("Sample already exists", 409)


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
