from datetime import datetime

from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti, jwt_required, get_jwt_identity
from flask_restful import fields, marshal, reqparse

from api import revoked_store
from api.constants import ACCESS_EXPIRES, REFRESH_EXPIRES
from api.models.database import BaseModel
from api.models.user import User
from api.resources.base_resource import BaseResource
from api.utils import get_user


class UserResource(BaseResource):
    fields = {
        'role_id': fields.Integer,
        'email': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    def get(self, **kwargs):
        if kwargs:
            print(kwargs.get('email'))
            email = kwargs.get('email')
            user = get_user(email)
            if user is None:
                return BaseResource.send_json_message("User not found", 404)
            else:
                data = marshal(user, self.fields)
                return BaseResource.send_json_message(data, 200)
        else:
            users = User.query.all()
            data = marshal(users, self.fields)
            return BaseResource.send_json_message(data, 200)

    def post(self):
        args = UserResource.user_parser()

        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']
        role = args['role']
        password = args['password']

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
                access_token = create_access_token(identity=user.email)
                refresh_token = create_refresh_token(identity=user.email)

                data = marshal(user, self.fields)
                data.update({"token": access_token})
                data.update({"refresh_token": refresh_token})
                data.update({"response": "Registered user"})

                # store the JWTs to redis with a status of not currently revoked.
                access_jti = get_jti(encoded_token=access_token)
                refresh_jti = get_jti(encoded_token=refresh_token)
                revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
                revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)

                return BaseResource.send_json_message(data, 201)
            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding User", 500)
        current_app.logger.error("Error while adding theme :> Duplicate records")
        return BaseResource.send_json_message('User already exists', 500)

    @jwt_required
    def put(self, email):
        args = UserResource.user_parser()

        first_name = args['first_name']
        last_name = args['last_name']
        user_email = args['email']
        role = int(args['role'])
        password = args['password']

        user = get_user(email)
        if user is not None:
            if first_name != user.first_name or last_name != user.last_name or \
                    user_email != user.email or role != user.role_id \
                    or not user.verify_password(password):

                try:
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = user_email
                    user.role_id = role
                    user.password = User.hash_password(password)
                    user.updated_at = datetime.now()
                    user.updated_by = get_jwt_identity()

                    BaseModel.db.session.commit()
                    return BaseResource.send_json_message("Updated user", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating user. Another user has that email", 500)
            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("User not found", 404)

    @jwt_required
    def delete(self, email):
        user = get_user(email)

        if not user:
            return BaseResource.send_json_message("User not found", 404)

        user.is_deleted = True
        user.deleted_at = datetime.now()
        user.deleted_by = get_jwt_identity()
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("User deleted", 200)

    @staticmethod
    def user_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', required=True)
        parser.add_argument('last_name', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('role', required=True)
        parser.add_argument('password', required=True)

        args = parser.parse_args()
        return args
