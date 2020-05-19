from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jti, \
    get_raw_jwt, jwt_refresh_token_required
from flask_restful import fields, reqparse, marshal

from api.constants import ACCESS_EXPIRES, REFRESH_EXPIRES, revoked_store
from api.resources.base_resource import BaseResource
from api.utils import non_empty_string, get_user_by_email, get_unconfirmed_user, get_deactivated_user


class AuthResource(BaseResource):
    fields = {
        'email': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
        'role.name': fields.String,
    }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", required=True, type=non_empty_string)
        parser.add_argument("password", required=True, type=non_empty_string)

        args = parser.parse_args()

        email = str(args['email']).lower()
        password = args['password']

        user = get_user_by_email(email)

        if user is None:
            # check if the user exists but their account is unconfirmed
            unconfirmed_user = get_unconfirmed_user(email)
            deactivated_user = get_deactivated_user(email)
            if unconfirmed_user:
                return BaseResource.send_json_message("User found but account not confirmed!", 203)
            elif deactivated_user:
                return BaseResource.send_json_message("", 204)
            return BaseResource.send_json_message("User not found", 404)

        elif user.verify_password(password):
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)

            data = marshal(user, self.fields)
            data.update({"token": access_token})
            data.update({"refresh_token": refresh_token})

            # store the JWTs to redis with a status of not currently revoked.
            access_jti = get_jti(encoded_token=access_token)
            refresh_jti = get_jti(encoded_token=refresh_token)
            revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
            revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)

            return BaseResource.send_json_message(data, 200)
        else:
            return BaseResource.send_json_message("Wrong password try again", 403)


class LogOutResource(BaseResource):
    @jwt_required
    def get(self):
        jti = get_raw_jwt()['jti']
        revoked_store.set(jti, 'true', ACCESS_EXPIRES * 1.2)
        return BaseResource.send_json_message("Successfully Logged Out", 200)

    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        revoked_store.set(jti, 'true', REFRESH_EXPIRES * 1.2)
        return BaseResource.send_json_message("Refresh token revoked", 200)
