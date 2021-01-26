import requests
from flask import request, current_app, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity

from api import BaseResource, BaseConfig
from api.models.database import BaseModel
from api.constants import REDCAP_URI, SAMPLE_FROM_FIELD, ADMIN_EMAIL
from api.models import Sample
from api.resources.email_confirmation.send_email import send_email
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

            # use python ternary operator to avoid errors
            user = None if AttributeError else get_user_by_email(sample['mail']).id
            # todo request staff-in-charge to enter email
            code = sample['sample_id']
            project = sample['project']
            location = {'lat': sample['lat'], 'long': sample['longitude']}
            owner = sample['staff_in_charge']  # todo: PI field not found
            sample_type = sample['sample_type_collected']

            if not Sample.sample_exists(code):
                sample = Sample(code=code, user_id=user, sample_type=sample_type, location_collected=location,
                                project=project, project_owner=owner, status=SAMPLE_FROM_FIELD)

                BaseModel.db.session.add(sample)
                BaseModel.db.session.commit()
                log_export_from_redcap(sample)
                continue

            log_duplicate(Sample.query.filter(Sample.code == code).first())
            # if an existing sample is encountered, do not return before finishing on other samples,
            # instead move control back to the for loop
            continue
        return BaseResource.send_json_message("Samples successfully fetched and saved", 201)


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
    html = render_template("redcap_error.html", user_email=user_email, user=user, error=error, admin_email=ADMIN_EMAIL)
    send_email(email, 'REDCap Error', template=html)
