from datetime import datetime

from flask import current_app, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import fields, marshal, reqparse

from api.models import Sample, Publication
from api.models.database import BaseModel
from api.models.user import User
from api.resources.base_resource import BaseResource
from api.resources.role_resource import RoleResource
from api.utils import get_active_users, get_user_by_email, get_users_by_role, get_users_by_status, get_deactivated_user, \
    log_in_user_jwt, format_and_lower_str, standard_non_empty_string, log_update


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
            return UserResource.UserCombinedInfo(email)
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
                BaseModel.db.session.add(user)
                BaseModel.db.session.commit()

                # LogIn User
                login = log_in_user_jwt(user)
                access_token = login.get('access_token')
                refresh_token = login.get('refresh_token')

                data = marshal(user, self.fields)
                data.update({"token": access_token})
                data.update({"refresh_token": refresh_token})
                data.update({"response": "Registered user"})
                current_app.logger.info("New user created;"
                                        "name={0}, email={1} at time={2}".format(first_name, email, datetime.now()))
                return BaseResource.send_json_message(data, 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding User", 500)

        elif deactivated_user is not None:
            deactivated_user.is_deleted = False
            deactivated_user.updated_at = datetime.now()
            deactivated_user.password = User.hash_password(password)
            deactivated_user.updated_by = get_jwt_identity() or deactivated_user.email
            BaseModel.db.session.commit()

            # LogIn User
            login = log_in_user_jwt(deactivated_user)
            access_token = login.get('access_token')
            refresh_token = login.get('refresh_token')

            data = marshal(deactivated_user, self.fields)
            data.update({"token": access_token})
            data.update({"refresh_token": refresh_token})
            data.update({"response": "Registered user"})
            current_app.logger.info("User's account has been activated;"
                                    "name={0}, email={1} at time={2}".format(first_name, email, datetime.now()))
            return BaseResource.send_json_message(data, 201)
        else:
            current_app.logger.error("Error while adding User :> Duplicate records")
            return BaseResource.send_json_message('User already exists', 409)

    @jwt_required
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
    def delete(self):
        email = format_and_lower_str(get_jwt_identity())
        user = get_user_by_email(email)

        if user is not None:
            if get_jwt_identity() != user.email:
                return BaseResource.send_json_message("Cannot delete another user", 403)

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
        elif type(user) is [] and len(user) >= 1:
            return BaseResource.send_json_message("Users not found", 404)
        else:
            data = marshal(user, UserResource.fields)
            return BaseResource.send_json_message(data, 200)

    @staticmethod
    def UserCombinedInfo(email):
        user = get_user_by_email(email)
        if user is None:
            return BaseResource.send_json_message("User not found", 404)
        else:
            user_details = {
                'fullname': user.first_name + " " + user.last_name,
                'email': user.email,
                'role': user.role.name
            }
            user_samples = BaseModel.db.session.query(Sample).filter(Sample.user_id == user.id).all()

            user_sample_details = []
            for sample in user_samples:
                sample_details = {}
                theme = sample.theme.name
                project = sample.project
                species = sample.animal_species
                _type = sample.sample_type
                barcode = sample.barcode

                sample_details.update(
                    {'theme': theme, 'project': project, 'species': species, 'type': _type, 'barcode': barcode})
                user_sample_details.append(sample_details)

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

            user_details.update({'samples': user_sample_details, 'publications': user_pub_details})
            return BaseResource.send_json_message(user_details, 200)
