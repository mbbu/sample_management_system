from flask import current_app, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, marshal, fields

from api.constants import PENDING_STATUS
from api.models import SampleRequest
from api.models.database import BaseModel
from api.resources.base_resource import BaseResource
from api.resources.email_confirmation.send_email import send_email
from api.resources.sample_resource import SampleResource
from api.utils import format_and_lower_str, log_create, log_update, log_delete, has_required_request_params, log_304, \
    get_user_by_email


class SampleRequestResource(BaseResource):
    fields = {
        'id': fields.Integer,
        'requester.first_name': fields.String,
        'requester.last_name': fields.String,
        'requester.email': fields.String,
        'requested_sample.project': fields.String,
        'requested_sample.animal_species': fields.String,
        'requested_sample.sample_type': fields.String,
        'requested_sample.location_collected': fields.String,
        'requested_sample.user.first_name': fields.String,
        'requested_sample.user.last_name': fields.String,
        'requested_sample.user.email': fields.String,
        'amount': fields.Integer,
        'request_date': fields.DateTime,
        'response_date': fields.DateTime,
        'status': fields.String,
        'notes': fields.String
    }

    def get(self):
        sample_requests = SampleRequest.query.all()
        data = marshal(sample_requests, self.fields)
        return BaseResource.send_json_message(data, 200)

    @jwt_required
    def post(self):
        args = SampleRequestResource.sample_request_parser()
        date = args['date'] if args['date'] is not None else "Unspecified date"
        amount = args['amount']
        user = get_user_by_email(get_jwt_identity())
        sample = SampleResource.get_sample(args['sample'])

        try:
            sample_request = SampleRequest(user=user.id, sample=sample.id, amount=amount, status=PENDING_STATUS)
            BaseModel.db.session.add(sample_request)
            BaseModel.db.session.commit()
            log_create(sample_request)

            storage = str(sample.box.tray.rack.chamber.freezer.lab.name) + ' Lab, freezer number ' + \
                      str(sample.box.tray.rack.chamber.freezer.number) + ' in a box labeled ' + str(sample.box.label)

            send_sample_request_email(email=sample.user.email, handler=sample.user.first_name,
                                      requester_name=user.first_name + ' ' + user.last_name,
                                      requester_email=user.email, species=sample.animal_species, qt=sample.quantity.id,
                                      sample_type=sample.sample_type, location=sample.location_collected,
                                      available=sample.amount, storage=storage, amount=amount, date=date)

            return BaseResource.send_json_message("Sample request made successfully", 201)

        except Exception as e:
            current_app.logger.error(e)
            BaseModel.db.session.rollback()
            return BaseResource.send_json_message("Error while making sample request", 500)

    @jwt_required
    @has_required_request_params
    def put(self):
        # todo: more modifications on sample request response
        code = format_and_lower_str(request.headers['code'])
        sample_request = SampleRequestResource.get_sample_request_with_pending_status(code)

        if sample_request is None:
            return BaseResource.send_json_message("Sample request cannot be edited!", 409)

        else:
            args = SampleRequestResource.sample_request_parser()
            amount = args['amount']
            user = get_user_by_email(get_jwt_identity())
            sample = SampleResource.get_sample(sample_request.requested_sample.code)

            if not args:
                # todo: send a reminder.
                return

            elif amount != sample_request.amount:
                old_info = str(sample_request)
                former_amount = str(sample_request.amount)

                try:
                    sample_request.amount = amount
                    BaseModel.db.session.commit()
                    log_update(old_info, sample_request)

                    send_sample_request_update_email(email=sample.user.email, handler=sample.user.first_name,
                                                     requester_name=user.first_name + ' ' + user.last_name,
                                                     requester_email=user.email, former_amount=former_amount,
                                                     available=sample.amount, amount=amount, qt=sample.quantity.id)

                    return BaseResource.send_json_message("Updated sample request successfully", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating sample request", 500)
            log_304(sample_request)
            return BaseResource.send_json_message("No changes made", 304)

    @jwt_required
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
        sample_request = SampleRequestResource.get_sample_request(code)

        if not sample_request:
            return BaseResource.send_json_message("Sample request not found", 404)

        BaseModel.db.session.delete(sample_request)
        BaseModel.db.session.commit()
        log_delete(sample_request)
        return BaseResource.send_json_message("Sample request deleted", 200)

    @staticmethod
    def sample_request_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('sample', required=True)
        parser.add_argument('amount', required=True)
        parser.add_argument('date', required=False)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_sample_request(code):
        return BaseModel.db.session.query(SampleRequest).filter_by(id=code).first()

    @staticmethod
    def get_sample_request_with_pending_status(code):
        return BaseModel.db.session.query(SampleRequest).filter_by(id=code, status=PENDING_STATUS).first()


def send_sample_request_email(email, handler, requester_name, requester_email, species, sample_type, location,
                              available, storage, amount, qt, date):
    html = render_template("sample_request.html",
                           requester_name=requester_name, requester_email=requester_email, qt=qt,
                           species=species, type=sample_type, location=location, handler=handler,
                           available_amount=available, storage=storage, amount=amount, date=date)
    send_email(email, 'Sample Request', template=html)


def send_sample_request_update_email(email, handler, requester_name, requester_email, former_amount,
                                     available, amount, qt):
    html = render_template("sample_request_update.html",
                           requester_name=requester_name, requester_email=requester_email, qt=qt,
                           handler=handler, former_amount=former_amount, available_amount=available, amount=amount)
    send_email(email, 'Sample Request', template=html)
