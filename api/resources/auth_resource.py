from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restful import fields, reqparse, marshal

from api.models.user import User
from api.resources.base_resource import BaseResource
from api.utils import non_empty_string


class AuthResource(BaseResource):
    fields = {
        'email': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
    }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, type=non_empty_string)
        parser.add_argument("password", required=True, type=non_empty_string)

        args = parser.parse_args()

        email = str(args['email'])
        password = args['password']

        user = User.query.filter(User.email == email).first()

        if user is None:
            return BaseResource.send_json_message("User not found", 404)

        elif user.verify_password(password):
            access_token = create_access_token(identity=user.email)
            data = marshal(user, self.fields)
            data.update({"token": access_token})
            return BaseResource.send_json_message(data, 200)
        else:
            return BaseResource.send_json_message("Wrong password try again", 403)


class UserLogOutResource(BaseResource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        if current_user:
            # session.clear()
            # todo: revoke token by using a blacklist
            return BaseResource.send_json_message("Successfully Logged Out", 200)
        return BaseResource.send_json_message("Error while logging out", 200)
