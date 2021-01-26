from flask import current_app, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse, marshal, fields

from api.constants import PENDING_STATUS, SAMPLE_REQUEST_RESPONSE, TOKEN_EXPIRATION_AS_DAYS, ADMIN_EMAIL
from api.models import SampleRequest
from api.models.database import BaseModel
from api.resources.base_resource import BaseResource
from api.resources.email_confirmation.send_email import send_email
from api.resources.sample_resource import SampleResource
from api.utils import format_and_lower_str, log_create, log_update, log_delete, has_required_request_params, log_304, \
    get_user_by_email, generate_confirmation_token, set_date_from_int, non_empty_int


class SampleRequestResource(BaseResource):
    fields = {
        'id': fields.Integer,
        'requester.first_name': fields.String,
        'requester.last_name': fields.String,
        'requester.email': fields.String,
        'requested_sample.project': fields.String,
        'requested_sample.animal_species': fields.String,
        'requested_sample.sample_type': fields.String,
        'requested_sample.study_block.name': fields.String,
        'requested_sample.study_block.area': fields.String,
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

            storage = str(sample.slot.box.tray.rack.chamber.freezer.lab.building) + ' Lab, freezer number ' + \
                      str(sample.slot.box.tray.rack.chamber.freezer.number) + \
                      ' in a box labeled ' + str(sample.slot.box.label) + ' and position ' + str(sample.slot.position)

            location = sample.study_block.name + ", " + sample.study_block.area

            send_sample_request_email(email=sample.user.email, handler=sample.user.first_name,
                                      requester_name=user.first_name + ' ' + user.last_name, requester_email=user.email,
                                      species=sample.animal_species, qt=sample.quantity.id,
                                      sample_type=sample.sample_type, location=location,
                                      available=sample.amount, storage=storage, amount=amount, date=date,
                                      sample_request=sample_request.id)

            return BaseResource.send_json_message("Sample request made successfully", 201)

        except Exception as e:
            current_app.logger.error(e)
            BaseModel.db.session.rollback()
            return BaseResource.send_json_message("Error while making sample request", 500)

    @jwt_required
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        sample_request = SampleRequestResource.get_sample_request_with_pending_status(code)

        if sample_request is None:
            return BaseResource.send_json_message("Sample request cannot be edited!", 409)

        else:
            args = SampleRequestResource.sample_request_parser()
            amount = args['amount']
            user = get_user_by_email(get_jwt_identity())
            sample = SampleResource.get_sample(sample_request.requested_sample.code)

            if request.headers['resend'] == 'resend':
                # SEND A REMINDER EMAIL TO SAMPLE HANDLER
                storage = str(sample.box.tray.rack.chamber.freezer.lab.name) + ' Lab, freezer number ' + \
                          str(sample.box.tray.rack.chamber.freezer.number) + ' in a box labeled ' + str(
                    sample.box.label)

                send_reminder_to_handler(email=sample.user.email, handler=sample.user.first_name,
                                         requester_name=user.first_name + ' ' + user.last_name,
                                         requester_email=user.email, species=sample.animal_species,
                                         qt=sample.quantity.id, sample_type=sample.sample_type,
                                         location=sample.location_collected, available=sample.amount,
                                         storage=storage, amount=sample_request.amount,
                                         sample_request=sample_request.id)

                return BaseResource.send_json_message("Email reminder sent", 200)

            # MAKE AN UPDATE TO THE SAMPLE AND NOTIFY THE HANDLER OF THE CHANGE
            elif request.headers['resend'] == 'update':
                if amount != sample_request.amount:
                    old_info = str(sample_request)
                    former_amount = str(sample_request.amount)

                    try:
                        sample_request.amount = amount
                        BaseModel.db.session.commit()
                        log_update(old_info, sample_request)

                        send_sample_request_update_email(email=sample.user.email, handler=sample.user.first_name,
                                                         requester_name=user.first_name + ' ' + user.last_name,
                                                         requester_email=user.email, former_amount=former_amount,
                                                         available=sample.amount, amount=amount, qt=sample.quantity.id,
                                                         sample_request=sample_request.id)

                        BaseModel.db.session.commit()
                        return BaseResource.send_json_message("Updated sample request successfully", 202)

                    except Exception as e:
                        current_app.logger.error(e)
                        BaseModel.db.session.rollback()
                        return BaseResource.send_json_message("Error while updating sample request", 500)
                log_304(sample_request)
                return BaseResource.send_json_message("No changes made", 304)
            return BaseResource.send_json_message("Not found", 404)

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
        parser.add_argument('amount', required=True, type=non_empty_int)
        parser.add_argument('date', required=False)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_sample_request(code):
        return BaseModel.db.session.query(SampleRequest).filter_by(id=code).first()

    @staticmethod
    def get_sample_request_with_pending_status(code):
        return BaseModel.db.session.query(SampleRequest).filter_by(id=code, status=PENDING_STATUS).first()


'''
    The functions below prepare an email to be sent to the sample handler. They receive;
        * email
        * handler
        * requester details
        * species
        * sample-type
        * location
        * available amount
        * storage
        * requested amount
        * the quantity type
        * date
        * sample
        
    In return it sets the token and updates the response url and passes the email to send_email function.
        
'''

expiration_date = set_date_from_int(TOKEN_EXPIRATION_AS_DAYS)


def send_sample_request_email(email, handler, requester_name, requester_email, species, sample_type, location,
                              available, storage, amount, qt, date, sample_request):
    sample_request_token = generate_confirmation_token(sample_request)
    sample_request_response_url = SAMPLE_REQUEST_RESPONSE.format(sample_request_token)

    html = render_template("sample_request.html",
                           requester_name=requester_name, requester_email=requester_email, qt=qt,
                           species=species, type=sample_type, location=location, handler=handler,
                           available_amount=available, storage=storage, amount=amount, date=date,
                           sample_request_response_url=sample_request_response_url,  admin_email=ADMIN_EMAIL,
                           expiration_days=TOKEN_EXPIRATION_AS_DAYS, expiration_date=expiration_date)
    send_email(email, 'Sample Request', template=html)


def send_sample_request_update_email(email, handler, requester_name, requester_email, former_amount,
                                     available, amount, qt, sample_request):
    sample_request_token = generate_confirmation_token(sample_request)
    sample_request_response_url = SAMPLE_REQUEST_RESPONSE.format(sample_request_token)

    html = render_template("sample_request_update.html",
                           requester_name=requester_name, requester_email=requester_email, qt=qt,
                           handler=handler, former_amount=former_amount, available_amount=available, amount=amount,
                           sample_request_response_url=sample_request_response_url,  admin_email=ADMIN_EMAIL,
                           expiration_days=TOKEN_EXPIRATION_AS_DAYS, expiration_date=expiration_date)
    send_email(email, 'Sample Request Update', template=html)


def send_reminder_to_handler(email, handler, requester_name, requester_email, species, sample_type, location,
                             available, storage, amount, qt, sample_request):
    sample_request_token = generate_confirmation_token(sample_request)
    sample_request_response_url = SAMPLE_REQUEST_RESPONSE.format(sample_request_token)

    html = render_template("sample_request_reminder.html",
                           requester_name=requester_name, requester_email=requester_email, qt=qt,
                           species=species, type=sample_type, location=location, handler=handler,
                           available_amount=available, storage=storage, amount=amount,
                           sample_request_response_url=sample_request_response_url, admin_email=ADMIN_EMAIL,
                           expiration_days=TOKEN_EXPIRATION_AS_DAYS, expiration_date=expiration_date)
    send_email(email, 'Sample Request Reminder', template=html)
