"""
    Password reset via email
"""
from datetime import datetime

from flask import current_app, render_template
from flask_restful import reqparse

from api import BaseResource, BaseModel
from api.constants import EXPIRATION_AS_HR
from api.models import User
from api.resources.email_confirmation.send_email import send_email
from api.utils import confirm_token, get_user_by_email, \
    generate_confirmation_token


# def generate_confirmation_token(email):
#     serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
#     return serializer.dumps(email, salt=BaseConfig.SECURITY_PASSWORD_SALT)
#
#
# def confirm_token(token, expiration=EMAIL_TOKEN_EXPIRATION):
#     serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
#     try:
#         email = serializer.loads(
#             token,
#             salt=BaseConfig.SECURITY_PASSWORD_SALT,
#             max_age=expiration
#         )
#     except Exception as e:
#         current_app.logger.error(e)
#         return False
#     return email


def send_confirmation_email(email):
    email_token = generate_confirmation_token(email)
    pwd_url = 'http://localhost:8080/reset/{0}'.format(email_token)
    html = render_template("password_reset.html", pwd_url=pwd_url, valid_time=EXPIRATION_AS_HR)
    send_email(email, 'Confirm Your Email Address', template=html)


# handle request to reset password
class ForgotPasswordResource(BaseResource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True)

        args = parser.parse_args()
        email = args['email']

        user = get_user_by_email(email)
        if user is None:
            return BaseResource.send_json_message('Sorry no user with given email', 404)
        send_confirmation_email(email)
        return BaseResource.send_json_message("Email sent", 200)


# handle actual reset password
class PasswordResetResource(BaseResource):
    def post(self, token):
        parser = reqparse.RequestParser()
        parser.add_argument('password', required=True)

        args = parser.parse_args()
        password = args['password']

        try:
            email = confirm_token(token)
            user = get_user_by_email(email)

            if user is None:
                return BaseResource.send_json_message('Sorry no user with given email', 404)
            else:
                user.password = User.hash_password(password)
                user.password_reset_on = datetime.now()
                BaseModel.db.session.commit()

            return BaseResource.send_json_message("Password reset successfully.", 200)

        except Exception:
            current_app.logger.error('The password rest link is invalid or has expired.')
            return BaseResource.send_json_message('The password rest link is invalid or has expired.'
                                                  '\nRequest another reset email', 408)
