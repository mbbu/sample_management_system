"""
    Email Confirmation
"""
from datetime import datetime

from flask import current_app, render_template
from flask_restful import marshal, fields
from itsdangerous import URLSafeTimedSerializer

from api import BaseResource, BaseModel
from api.config import BaseConfig
from api.constants import EMAIL_TOKEN_EXPIRATION
from api.resources.email_confirmation.send_email import send_email
from api.utils import log_in_user_jwt, get_unconfirmed_user


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    return serializer.dumps(email, salt=BaseConfig.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=EMAIL_TOKEN_EXPIRATION):
    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=BaseConfig.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except Exception as e:
        current_app.logger.error(e)
        return False
    return email


def send_confirmation_email(email):
    email_token = generate_confirmation_token(email)
    confirm_url = 'http://localhost:8080/confirm/{0}'.format(email_token)
    html = render_template("email_confirmation.html", confirm_url=confirm_url, valid_time=EMAIL_TOKEN_EXPIRATION)
    send_email(email, 'Confirm Your Email Address', template=html)


class EmailConfirmationResource(BaseResource):
    fields = {
        'role.name': fields.String,
        'email': fields.String,
        'first_name': fields.String,
        'last_name': fields.String
    }

    def get(self, token):
        try:
            email = confirm_token(token)
            user = get_unconfirmed_user(email)

            if user is None:
                return BaseResource.send_json_message('Account already confirmed.', 404)
            else:
                user.email_confirmed = True
                user.is_active = True
                user.email_confirmed_on = datetime.now()
                BaseModel.db.session.commit()

                # LogIn User
                login = log_in_user_jwt(user)
                access_token = login.get('access_token')
                refresh_token = login.get('refresh_token')

                data = marshal(user, self.fields)
                data.update({"token": access_token})
                data.update({"refresh_token": refresh_token})
                data.update({"response": "Account confirmed!"})

            return BaseResource.send_json_message(data, 200)

        except Exception:
            current_app.logger.error('The confirmation link for is invalid or has expired.')
            return BaseResource.send_json_message('The confirmation link is invalid or has expired.'
                                                  '\nRequest another confirmation email', 408)
