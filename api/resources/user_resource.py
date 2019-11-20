from flask import current_app

from api.resources.base_resource import BaseResource
from api.models.database import BaseModel
from api.models.user import User

from flask_restful import fields, marshal, reqparse


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
