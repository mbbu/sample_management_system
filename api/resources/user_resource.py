from datetime import datetime

from flask import current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import fields, marshal, reqparse

from api.models import Sample, Publication, SampleRequest
from api.models.database import BaseModel
from api.models.user import User
from api.resources.base_resource import BaseResource
from api.resources.decorators.user_role_decorators import authorized_to_modify_user
from api.resources.email_confirmation.email_confirmation import send_confirmation_email
from api.resources.role_resource import RoleResource
from api.utils import get_active_users, get_user_by_email, get_users_by_role, get_users_by_status, get_deactivated_user, \
    format_and_lower_str, standard_non_empty_string, log_update


class UserResource(BaseResource):
    fields = {
        'role.name': fields.String,
        'email': fields.String,
        'first_name': fields.String,
        'last_name': fields.String
    }

    def get(self):
        email = request.headers.get('email')
        role = request.headers.get('role')
        deleted = request.headers.get('deleted')

        if email is not None:
            email = format_and_lower_str(email)
            return UserResource.user_combined_info(email)
        elif role is not None:
            users = get_users_by_role(role)
            return UserResource.get_response(users)
        elif deleted is not None:
            deleted = str.capitalize(deleted)
            users = get_users_by_status(deleted)
            return UserResource.get_response(users)
        else:
            users = get_active_users()
            return UserResource.get_response(users)

    def post(self):
        args = UserResource.user_parser()

        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']
        password = args['password']

        # FK
        db_role = RoleResource.get_role(args['role'])
        role = db_role.id

        deactivated_user = get_deactivated_user(email)

        if not User.user_exists(email):
            try:
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    role_id=role,
                    password=User.hash_password(password),
                    created_by=email
                )

                current_app.logger.info("New user created;"
                                        "name={0}, email={1} at time={2}".format(first_name, email, datetime.now()))

                # Confirm user registration details
                send_confirmation_email(user.email)
                user.email_confirmation_sent_on = datetime.now()

                BaseModel.db.session.add(user)
                BaseModel.db.session.commit()

                return BaseResource.send_json_message("User registered. Account confirmation pending!", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding User", 500)

        elif deactivated_user is not None:
            deactivated_user.is_active = True
            deactivated_user.deactivated_at = None
            deactivated_user.deactivated_by = None
            deactivated_user.reactivated_at = datetime.now()
            deactivated_user.reactivated_by = get_jwt_identity() or deactivated_user.email
            deactivated_user.password = User.hash_password(password)
            BaseModel.db.session.commit()

            current_app.logger.info("User's account has been activated;"
                                    "name={0}, email={1} at time={2}".format(first_name, email, datetime.now()))
            return BaseResource.send_json_message("Account reactivated. Please login to continue.", 201)
        else:
            current_app.logger.error("Error while adding User :> Duplicate records")
            return BaseResource.send_json_message('User already exists', 409)

    @jwt_required
    @authorized_to_modify_user
    def put(self):
        email = format_and_lower_str(get_jwt_identity())
        user = get_user_by_email(email)

        if user is not None:
            if get_jwt_identity() != user.email:
                current_app.logger.info("{0} trying to update {1}!".format(get_jwt_identity(), user.email))
                return BaseResource.send_json_message("Cannot update another user", 403)

            else:
                args = UserResource.user_parser()

                first_name = args['first_name']
                last_name = args['last_name']
                user_email = args['email']
                role = int(args['role'])

                if first_name != user.first_name or last_name != user.last_name or \
                        user_email != user.email or role != user.role_id:
                    old_info = str(user)
                    try:
                        user.first_name = first_name
                        user.last_name = last_name
                        user.email = user_email
                        user.role_id = role
                        user.updated_at = datetime.now()
                        user.updated_by = user.email

                        BaseModel.db.session.commit()
                        log_update(old_info, user)
                        return BaseResource.send_json_message("Updated user", 202)

                    except Exception as e:
                        current_app.logger.error(e)
                        BaseModel.db.session.rollback()
                        return BaseResource.send_json_message("Error while updating user. Another user has that email",
                                                              409)

                return BaseResource.send_json_message("No changes made", 304)
        current_app.logger.info("{0} trying to update {1} but does not exist".format(get_jwt_identity(), email))
        return BaseResource.send_json_message("User not found", 404)

    @jwt_required
    @authorized_to_modify_user
    def delete(self):
        email = format_and_lower_str(get_jwt_identity())
        user = get_user_by_email(email)

        if user is not None:
            # decide whether to delete user or deactivate account.
            # How? Check for deactivate in headers

            if request.headers.get('deactivate'):
                user.is_active = False
                user.deactivated_at = datetime.now()
                user.deactivated_by = email
                user.reactivated_at = None
                user.reactivated_by = None
                BaseModel.db.session.commit()
                current_app.logger.info("{0} deactivated {1}".format(get_jwt_identity(), user.email))
                return BaseResource.send_json_message("User account deactivated", 200)
            else:
                user.is_deleted = True
                user.deleted_at = datetime.now()
                user.deleted_by = get_jwt_identity()
                BaseModel.db.session.commit()
                current_app.logger.info("{0} deleted {1}".format(get_jwt_identity(), user.email))
                return BaseResource.send_json_message("User deleted", 200)

        current_app.logger.info("{0} trying to delete {1} but does not exist".format(get_jwt_identity(), email))
        return BaseResource.send_json_message("User not found", 404)

    @staticmethod
    def user_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', required=True)
        parser.add_argument('last_name', required=True)
        parser.add_argument('email', required=True, type=standard_non_empty_string)
        parser.add_argument('role', required=True)
        parser.add_argument('password', required=False)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_response(user):
        if user is None:
            return BaseResource.send_json_message("User not found", 404)
        elif type(user) is list and len(user) < 1:
            return BaseResource.send_json_message("Users not found", 404)
        else:
            data = marshal(user, UserResource.fields)
            return BaseResource.send_json_message(data, 200)

    @staticmethod
    def user_combined_info(email):
        user = get_user_by_email(email)
        if user is None:
            return BaseResource.send_json_message("User not found", 404)
        else:
            ############################################################################################################
            #           user details to return to make their profile                                                   #
            ############################################################################################################
            user_details = {
                'fullname': user.first_name + " " + user.last_name,
                'email': user.email,
                'role': user.role.name
            }

            ############################################################################################################
            #                  samples belonging to user                                                               #
            ############################################################################################################
            user_samples = BaseModel.db.session.query(Sample).filter(Sample.user_id == user.id).all()

            user_sample_details = []
            for sample in user_samples:
                sample_details = {}
                theme = sample.theme.name
                project = sample.project
                species = sample.animal_species
                _type = sample.sample_type
                barcode = sample.barcode
                code = sample.code
                location = sample.location_collected

                sample_details.update(
                    {'theme': theme, 'project': project, 'species': species, 'type': _type,
                     'barcode': barcode, 'code': code, 'location': location})
                user_sample_details.append(sample_details)

            ############################################################################################################
            #                publications belonging to user                                                            #
            ############################################################################################################
            user_publications = BaseModel.db.session.query(Publication).filter(Publication.user_id == user.id).all()

            user_pub_details = []
            for publication in user_publications:
                publications = {}
                title = publication.publication_title
                co_authors = publication.co_authors
                project = publication.sample.project
                theme = publication.sample.theme.name

                publications.update({'theme': theme, 'project': project, 'title': title, 'co_authors': co_authors})
                user_pub_details.append(publications)

            ############################################################################################################
            #                        sample requests belonging to user                                                 #
            ############################################################################################################
            user_sample_requests = BaseModel.db.session.query(SampleRequest) \
                .filter(SampleRequest.user == user.id).all()

            user_sample_request_details = []
            for sample_request in user_sample_requests:
                sample_requests = {}
                sample_owner = sample_request.requested_sample.project_owner
                sample_project = sample_request.requested_sample.project
                sample_type = sample_request.requested_sample.sample_type
                sample_species = sample_request.requested_sample.animal_species
                amount = sample_request.amount
                request_date = sample_request.request_date.strftime("%d-%m-%Y %H:%M")
                response_date = None if AttributeError else sample_request.response_date.strftime(
                    "%d-%m-%Y %H:%M")  # todo python type errors not checked this way
                status = sample_request.status
                code = sample_request.id
                notes = sample_request.notes
                approved = sample_request.approved_amount

                sample_requests.update({'type': sample_type, 'species': sample_species, 'amount': amount,
                                        'request_date': request_date, 'response_date': response_date, 'code': code,
                                        'status': status, 'owner': sample_owner, 'project': sample_project,
                                        'notes': notes, 'approved': approved})
                user_sample_request_details.append(sample_requests)

            ############################################################################################################
            #           requested samples belonging to user                                                            #
            ############################################################################################################
            user_requested_samples = BaseModel.db.session.query(SampleRequest).join(Sample) \
                .filter(Sample.user_id == user.id).all()

            user_requested_samples_details = []
            for sample_request in user_requested_samples:
                requested_samples = {}
                sample_owner = sample_request.requested_sample.project_owner
                sample_project = sample_request.requested_sample.project
                sample_type = sample_request.requested_sample.sample_type
                sample_species = sample_request.requested_sample.animal_species
                amount = sample_request.amount
                request_date = sample_request.request_date.strftime("%d-%m-%Y %H:%M")
                response_date = None if AttributeError else sample_request.response_date.strftime(
                    "%d-%m-%Y %H:%M")  # todo python type errors not checked this way
                status = sample_request.status
                code = sample_request.id
                notes = sample_request.notes
                approved = sample_request.approved_amount

                requested_samples.update({'type': sample_type, 'species': sample_species, 'amount': amount,
                                          'request_date': request_date, 'response_date': response_date, 'code': code,
                                          'status': status, 'owner': sample_owner, 'project': sample_project,
                                          'notes': notes, 'approved': approved})
                user_requested_samples_details.append(requested_samples)

            user_details.update({'samples': user_sample_details, 'publications': user_pub_details,
                                 'sample_requests': user_sample_request_details,
                                 'requested_samples': user_requested_samples_details})

            return BaseResource.send_json_message(user_details, 200)
