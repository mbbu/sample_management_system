from datetime import datetime

from flask import current_app
from flask_jwt_extended import jwt_required
from flask_restful import reqparse

from api import BaseResource
from api.constants import APPROVED_STATUS, DECLINED_STATUS
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
            sample_request_id = confirm_token(token)
            sample_request = SampleRequestResource.get_sample_request_with_pending_status(sample_request_id)

            if sample_request is None:
                return BaseResource.send_json_message('Sample request not found.', 404)
            else:
                args = SampleRequestResponseResource.sample_request_response_parser()
                status = args['status']
                notes = args['notes']

                # todo: send email;
                if status == 'APPROVED':
                    status = APPROVED_STATUS
                    # todo: to requester
                    # todo: to L.I.M.S
                elif status == 'DECLINED':
                    status = DECLINED_STATUS
                    # todo: to requester

                sample_request.notes = notes
                sample_request.status = status
                sample_request.response_date = datetime.now()

                return BaseResource.send_json_message('Response registered and requester notified', 200)
        except Exception as e:
            current_app.logger.error('The link for is invalid or has expired.' + str(e))
            return BaseResource.send_json_message('The link is invalid or has expired!'
                                                  ' Ask the requester to resend request', 408)

    @staticmethod
    def sample_request_response_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('status', required=True)
        parser.add_argument('notes', required=True)

        args = parser.parse_args()
        return args
