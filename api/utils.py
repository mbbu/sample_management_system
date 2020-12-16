from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

from faker import Faker
from flask import current_app, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti, get_jwt_identity
from flask_restful import marshal, fields
from itsdangerous import URLSafeTimedSerializer
from mixer.backend.flask import Mixer

from api import revoked_store, BaseResource
from api.config import BaseConfig
from api.constants import ACCESS_EXPIRES, REFRESH_EXPIRES, EMAIL_TOKEN_EXPIRATION, TOKEN_EXPIRATION
from api.models import *
from api.models.database import BaseModel

"""
    Parser formatting methods for json fields sent in request. Plays the same role as 
    the form validation methods.    
"""


def non_empty_string(s: str):
    if not s.strip():
        raise ValueError("Expected a non empty string")
    return s.strip()


def standard_non_empty_string(s: str):
    if not s:
        raise ValueError("Expected a non empty string")
    return format_and_lower_str(s)


def format_and_lower_str(string):
    return str(string).strip().lower()


def non_empty_int(i: int):
    if not i:
        raise ValueError("Expected an integer")
    return i


"""
    Date Formatter
"""


def format_str_to_date(_date):
    """
    Function takes a date string and converts it to a date object
    :param _date:
    :return:
    """
    return datetime.strptime(_date, '%Y-%m-%d %H:%M').date()


def set_date_from_int(num_of_days):
    """
    Function increments date by number of days passed
    :param num_of_days:
    :return: date
    """
    date = datetime.now()

    for day in range(num_of_days):
        date = date + timedelta(days=1)
    return date


"""
    Functions for requesting user resources. 
"""


def get_any_user_by_email(email):
    return BaseModel.db.session.query(User).filter(User.email == email).first()


def get_active_users():
    return BaseModel.db.session.query(User).filter(User.is_deleted == False).all()


def get_user_by_email(email):
    return BaseModel.db.session.query(User).filter(User.email == email, User.is_deleted == False,
                                                   User.is_active == True, User.email_confirmed == True).first()


def get_unconfirmed_user(email):
    return BaseModel.db.session.query(User).filter(User.email == email, User.is_active == False,
                                                   User.email_confirmed == False).first()


def get_deactivated_user(email):
    return BaseModel.db.session.query(User).filter(User.email == email, User.is_active == False,
                                                   User.is_deleted == False).first()


def get_users_by_role(role):
    return BaseModel.db.session.query(User).filter(User.role_id == role, User.is_deleted == False).all()


def get_users_by_status(status):
    return BaseModel.db.session.query(User).filter(User.is_deleted == status).all()


def log_in_user_jwt(user):
    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    # store the JWTs to redis with a status of not currently revoked.
    access_jti = get_jti(encoded_token=access_token)
    refresh_jti = get_jti(encoded_token=refresh_token)
    revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
    revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)

    return {'access_token': access_token, 'refresh_token': refresh_token}


def get_sample_by_code(code):
    return BaseModel.db.session.query(Sample).filter(Sample.code == code).first()


"""
    Logging Functions
"""


def log_304(record):
    return current_app.logger.info("No changes were made to {0}".format(record))


def log_create(record):
    return current_app.logger.info(
        "New {0} created by {1} at {2}".format(record, get_jwt_identity(), datetime.now()))


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


fake = Faker()

"""
    Functions for token generation and confirmation
"""


def generate_confirmation_token(known_var):
    """
    :arg: some known variable that is to be kept secret
    :param known_var:
    :return: serialized token
    """
    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    return serializer.dumps(known_var, salt=BaseConfig.SECURITY_PASSWORD_SALT)


def confirm_token(token):
    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=BaseConfig.SECURITY_PASSWORD_SALT,
            max_age=EMAIL_TOKEN_EXPIRATION
        )
        return email
    except Exception as e:
        current_app.logger.error(e)
    try:
        known_var = serializer.loads(
            token,
            salt=BaseConfig.SECURITY_PASSWORD_SALT,
            max_age=TOKEN_EXPIRATION
        )
        return known_var
    except Exception as e:
        current_app.logger.error(e)


def get_query_params():
    """
    function gets the current url of the request object and parses it to get the query string. It is returned here as a
    dictionary, so the function gets the value of the key i.e. q which is the query passed in the url
    :return:
    """
    url = request.url

    parsed_url = urlparse(url)
    query = parse_qs(parsed_url.query)

    return query.get('q')


def get_chambers(f):
    field = {
        'type': fields.String,
        'freezer.number': fields.String,
        'code': fields.String
    }
    chambers = BaseModel.db.session.query(Chamber).filter_by(freezer_id=f).all()
    return marshal(chambers, field)


def get_racks(c):
    field = {
        'chamber.type': fields.String,
        'number': fields.String,
        'code': fields.String
    }
    racks = BaseModel.db.session.query(Rack).filter_by(chamber_id=c).all()
    return marshal(racks, field)


def get_trays(r):
    field = {
        'number': fields.String,
        'rack.number': fields.String,
        'code': fields.String
    }
    trays = BaseModel.db.session.query(Tray).filter_by(rack_id=r).all()
    return marshal(trays, field)


def get_boxes(b):
    field = {
        'label': fields.String,
        'code': fields.String,
    }
    boxes = BaseModel.db.session.query(Box).filter_by(tray_id=b).all()
    return marshal(boxes, field)


def get_slots(s):
    field = {
        'position': fields.Raw,
        'code': fields.String,
        'available': fields.Boolean,
    }

    slots = BaseModel.db.session.query(Slot).filter_by(box_id=s).all()
    return marshal(slots, field)
