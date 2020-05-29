"""
    These decorator functions check the user role and return true or false appropriately

"""
from flask import request
from flask_jwt_extended import get_jwt_identity

from api import BaseResource
from api.constants import SYSADMIN, FORBIDDEN_FUNCTION_ACCESS_RESPONSE, FORBIDDEN_FUNCTION_ACCESS_RESPONSE_CODE, \
    THEMEADMIN
from api.models import User, Sample, Role
from api.utils import get_user_by_email


def is_sys_admin(admin_restricted_func):
    """
    Decorator func to check if the user is the admin before executing a function
    :param admin_restricted_func:
    :return:
    """

    def wrapper(*args, **kwargs):
        user_id = get_user_by_email(get_jwt_identity()).id
        admin = User.query.join(Role).filter(User.id == user_id, Role.code == SYSADMIN).first()
        if not admin:
            return BaseResource.send_json_message(FORBIDDEN_FUNCTION_ACCESS_RESPONSE,
                                                  FORBIDDEN_FUNCTION_ACCESS_RESPONSE_CODE)
        return admin_restricted_func(*args, **kwargs)

    return wrapper


def is_theme_admin(theme_admin_restricted_func):
    """
    Decorator func to check if the user is the admin before executing a function
    :param theme_admin_restricted_func:
    :return:
    """

    def wrapper(*args, **kwargs):
        user_id = get_user_by_email(get_jwt_identity()).id
        theme_admin = User.query.join(Role).filter(User.id == user_id, Role.code == THEMEADMIN).first()
        sys_admin = User.query.join(Role).filter(User.id == user_id, Role.code == SYSADMIN).first()
        if not theme_admin or not sys_admin:
            return BaseResource.send_json_message(FORBIDDEN_FUNCTION_ACCESS_RESPONSE,
                                                  FORBIDDEN_FUNCTION_ACCESS_RESPONSE_CODE)
        return theme_admin_restricted_func(*args, **kwargs)

    return wrapper


def is_sample_owner(sample_restricted_func):
    """
    Decorator func to check if the user is the admin before executing a function
    :param sample_restricted_func:
    :return:
    """

    def wrapper(*args, **kwargs):
        user_id = get_user_by_email(get_jwt_identity()).id

        # check if they are sample owners
        user_samples = Sample.query.filter(Sample.user_id == user_id).all()
        this_sample_code = request.headers['code']
        sample_owner = False

        for sample in user_samples:
            if sample.code == this_sample_code:
                sample_owner = True
                break
            else:
                sample_owner = False
                break

        # check if they are either a system admin or theme admin
        sys_admin = User.query.join(Role).filter(User.id == user_id, Role.code == SYSADMIN).first()
        theme_admin = User.query.join(Role).filter(User.id == user_id, Role.code == THEMEADMIN).first()

        if not sample_owner and theme_admin is None and sys_admin is None:
            return BaseResource.send_json_message("Cannot access this function, you are not the sample owner",
                                                  FORBIDDEN_FUNCTION_ACCESS_RESPONSE_CODE)
        return sample_restricted_func(*args, **kwargs)
    return wrapper
