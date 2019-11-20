from flask import current_app
from flask_restful import fields, marshal, reqparse

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
    }

    def get(self):
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
                    password=User.hash_password(password)
                )

                BaseModel.db.session.add(user)
                BaseModel.db.session.commit()
                return BaseResource.send_json_message('Registered user', 201)
            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding User", 500)
        current_app.logger.error("Error while adding theme :> Duplicate records")
        return BaseResource.send_json_message('User already exists', 500)

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

                    BaseModel.db.session.commit()
                    return BaseResource.send_json_message("Updated user", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating user. Another user has that email", 500)
            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("User not found", 404)

    def delete(self, email):
        user = get_user(email)

        if not user:
            return BaseResource.send_json_message("User not found", 404)

        BaseModel.db.session.delete(user)
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
