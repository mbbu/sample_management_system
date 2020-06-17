import requests
from flask import request, current_app, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity

from api import BaseResource, BaseModel, BaseConfig
from api.constants import REDCAP_URI
from api.models import Sample
from api.resources.box_resource import BoxResource
from api.resources.email_confirmation.send_email import send_email
from api.resources.theme_resource import ThemeResource
from api.utils import log_export_from_redcap, log_duplicate, get_user_by_email


class SaveSampleFromREDCap(BaseResource):
    @jwt_required
    def get(self):
        sample_records = export_all_records()

        if exception is not None:
            current_user = get_user_by_email(get_jwt_identity())
            user = current_user.first_name + " " + current_user.last_name
            user_email = get_user_by_email(get_jwt_identity()).email
            send_email_on_redcap_issue(email=BaseConfig.ADMINS, error=exception, user=user, user_email=user_email)
            return BaseResource.send_json_message("Redcap error. Admin contacted.", 500)
        elif not sample_records:
            return BaseResource.send_json_message("No sample records found", 404)
        else:
            return SaveSampleFromREDCap.save_all_samples(sample_records)

    @staticmethod
    def save_all_samples(sample_records):
        for sample in sample_records:
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

            user = None if AttributeError else get_user_by_email(sample['mail']).id
            # todo: if user is not assigned, then assign it either to admin or theme admin
            sample_type = sample['sample_type_collected']
            project = sample['project']
            box = None if AttributeError else BoxResource.get_box(sample['box_id']).id
            theme = None if AttributeError else ThemeResource.get_theme(sample['theme']).id
            code = sample['sample_id']
            amount = None if ValueError else int(sample['amount'])
            location = {'lat': sample['lat'], 'long': sample['longitude']}
            owner = sample['staff_in_charge']

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
exception = None


def export_all_records():
    token = request.headers.get('token')
    data = {
        'token': BaseConfig.REDCap_API_TOKEN or token,
        'content': 'record',
        'format': 'json',
        'returnFormat': 'json'
    }

    try:
        response = requests.post(REDCAP_URI, data)
        return response.json()

    except Exception as e:
        current_app.logger.error(e)
        global exception
        exception = e
        return exception


def send_email_on_redcap_issue(email, error, user, user_email):
    html = render_template("redcap_error.html", user_email=user_email, user=user, error=error)
    send_email(email, 'REDCap Error', template=html)
