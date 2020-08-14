from datetime import datetime

from flask import current_app, render_template, request
from flask_jwt_extended import jwt_required
from flask_restful import reqparse

from api import BaseResource, BaseModel
from api.constants import APPROVED_STATUS, DECLINED_STATUS
from api.resources.email_confirmation.send_email import send_email
from api.resources.sample_request_and_response.sample_request_resource import SampleRequestResource
from api.utils import confirm_token

"""
    on response, update the request with the appropriate details i.e.
        *   status
        *   response_date
        *   notes
        
    Then send emails to relevant parties i.e.
        * To the requester to notify then of the response
        * To the L.I.M.S if the request is approved
"""


class SampleRequestResponseResource(BaseResource):
    @jwt_required
    def put(self, token):
        try:
            sample_request_id = request.headers.get('code') if not None else confirm_token(token)
            sample_request = SampleRequestResource.get_sample_request_with_pending_status(sample_request_id)

            if sample_request is None:
                return BaseResource.send_json_message('Sample request not found.', 404)
            else:
                args = SampleRequestResponseResource.sample_request_response_parser()
                status = args['status']
                notes = args['notes']
                approved_amount = int(args['approved_amount'])

                if status == 'APPROVED':
                    status = APPROVED_STATUS
                    # todo: to L.I.M.S
                elif status == 'DECLINED':
                    status = DECLINED_STATUS

                sample_request.notes = notes
                sample_request.status = status
                sample_request.approved_amount = approved_amount
                sample_request.requested_sample.amount = sample_request.requested_sample.amount - approved_amount
                sample_request.response_date = datetime.now()

                # send email to requester

                storage = str(sample_request.requested_sample.box.tray.rack.chamber.freezer.lab.name) \
                          + ' Lab, freezer number ' + str(
                    sample_request.requested_sample.box.tray.rack.chamber.freezer.number) + ' in a box labeled ' + str(
                    sample_request.requested_sample.box.label)

                species = sample_request.requested_sample.animal_species
                _type = sample_request.requested_sample.sample_type
                location = sample_request.requested_sample.location_collected
                qt = sample_request.requested_sample.quantity.id

                send_response_on_request_status(email=sample_request.requester.email, notes=notes, qt=qt,
                                                status=status, approved_amount=approved_amount,
                                                requester_name=sample_request.requester.first_name + ' '
                                                               + sample_request.requester.last_name,
                                                species=species, _type=_type, location=location, storage=storage)

                BaseModel.db.session.commit()
                return BaseResource.send_json_message('Response registered and requester notified', 200)
        except Exception as e:
            current_app.logger.error('The link for is invalid or has expired.' + str(e))
            return BaseResource.send_json_message('The link is invalid or has expired!'
                                                  ' Ask the requester to resend request', 408)

    @staticmethod
    def sample_request_response_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('status', required=True)
        parser.add_argument('notes', required=False)
        parser.add_argument('approved_amount', required=False)

        args = parser.parse_args()
        return args


def send_response_on_request_status(email, requester_name, status, notes, approved_amount, qt, species, _type, storage,
                                    location):
    title = ""
    if status == APPROVED_STATUS:
        title = "Request Granted"
    elif status == DECLINED_STATUS:
        title = "Request Declined"

    # todo: lims url
    lims_url = '/'
    html = render_template('sample_request_response.html', requester_name=requester_name, status=status, notes=notes,
                           lims_url=lims_url, approved_amount=approved_amount, storage=storage, species=species, qt=qt,
                           type=_type, location=location, approved=APPROVED_STATUS, declined=DECLINED_STATUS)

    send_email(email, title, template=html)
