from datetime import datetime

import requests
from flask import current_app, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti, get_jwt_identity
from mixer.backend.flask import Mixer

from api import revoked_store, BaseResource
from api.config import BaseConfig
from api.constants import ACCESS_EXPIRES, REFRESH_EXPIRES, REDCAP_URI
from api.models import *
from api.models.database import BaseModel

"""
    Parser formatting methods for json fields sent in request. Plays the same role as 
    the form validation methods.    
"""


def non_empty_string(s: str):
    if not s:
        raise ValueError("Expected a non empty string")
    return s


def non_empty_int(i: int):
    if not i:
        raise ValueError("Expected an integer")
    return i


"""
    Functions for requesting user resources. 
"""


def get_active_users():
    return BaseModel.db.session.query(User).filter(User.is_deleted == False).all()


def get_user_by_email(email):
    return BaseModel.db.session.query(User).filter(User.email == email, User.is_deleted == False).first()


def get_users_by_role(role):
    return BaseModel.db.session.query(User).filter(User.role_id == role, User.is_deleted == False).all()


def get_users_by_status(status):
    return BaseModel.db.session.query(User).filter(User.is_deleted == status).all()


def get_deactivated_user(email):
    return BaseModel.db.session.query(User).filter(User.email == email, User.is_deleted == True).first()


def log_in_user_jwt(user):
    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    # store the JWTs to redis with a status of not currently revoked.
    access_jti = get_jti(encoded_token=access_token)
    refresh_jti = get_jti(encoded_token=refresh_token)
    revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
    revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)

    return {'access_token': access_token, 'refresh_token': refresh_token}


def get_samples_by_code(code):
    return BaseModel.db.session.query(Sample).filter(Sample.is_deleted == code).all()


"""
    String formatters
"""


def format_and_lower_str(string):
    return str(string).strip().lower()


"""
    Date Formatter
"""


def format_str_to_date(date):
    return datetime.strptime(date, '%Y-%m-%d %H:%M').date()


"""
    Logging Functions
"""


def log_304():
    return current_app.logger.info("No changes were made")


def log_create(record):
    return current_app.logger.info(
        "New {0} created by {1} at {2}".format(record, get_jwt_identity(), datetime.now()))


# todo: log old value and new value
def log_update(old_record, new_record):
    return current_app.logger.info("{0} updated {1} to {2} at time={3}"
                                   .format(get_jwt_identity(), old_record, new_record,
                                           datetime.now()))


def log_delete(record):
    return current_app.logger.info("{0} deleted {1} at {2}".format(get_jwt_identity(), record, datetime.now()))


def log_duplicate(record):
    return current_app.logger.error("Error while adding {0} :> Duplicate records".format(record))


def log_export_from_redcap(record):
    return current_app.logger.info(
        "New sample {0} created from REDCap at {1} by {2}".format(record, datetime.now(), get_jwt_identity()))


"""
   Decorator functions
"""


def has_required_request_params(record_identity):
    def wrapper(*args, **kwargs):
        if (request.headers.get('code') or request.headers.get('label') or request.headers.get('title')) is None:
            return BaseResource.send_json_message(
                "Expected an identifier i.e code or label to perform action. Pass the same in request header", 400)
        return record_identity(*args, **kwargs)

    return wrapper


"""
    REDCap API functions
"""


# fetch all records
def export_all_records():
    token = request.headers.get('token')
    data = {
        'token': BaseConfig.REDCap_API_TOKEN or token,
        'content': 'record',
        'format': 'json',
        'returnFormat': 'json'
    }
    response = requests.post(REDCAP_URI, data)

    if response.status_code == 200:
        return response.json()
    return 404


"""
    Faker function; helps to create new random records in the database. 
    takes two argument;
        a) count - number of records to create
        b) model - the model to create records for
"""


def faker(count, model, model_name):
    _mixer = Mixer(commit=False)
    for num in range(0, count):
        record = _mixer.blend(model)

        BaseModel.db.session.add(record)
        BaseModel.db.session.commit()
        num += 1

    return BaseResource.send_json_message("{}s created".format(model_name), 200)
