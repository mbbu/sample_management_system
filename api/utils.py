from flask_jwt_extended import create_access_token, create_refresh_token, get_jti

from api import revoked_store
from api.constants import ACCESS_EXPIRES, REFRESH_EXPIRES
from api.models.database import BaseModel
from api.models.user import User


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


def log_in_user_jwt(user):
    access_token = create_access_token(identity=user.email)
    refresh_token = create_refresh_token(identity=user.email)

    # store the JWTs to redis with a status of not currently revoked.
    access_jti = get_jti(encoded_token=access_token)
    refresh_jti = get_jti(encoded_token=refresh_token)
    revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
    revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)

    return {'access_token': access_token, 'refresh_token': refresh_token}

