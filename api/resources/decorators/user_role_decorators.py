"""
    These decorator functions check the user role and return true or false appropriately

"""
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
        if not theme_admin or not is_sys_admin:
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
        sample_owner = Sample.query.filter(Sample.user_id == user_id).first()
        if not (sample_owner or is_theme_admin or is_sys_admin):
            return BaseResource.send_json_message("Cannot access this function, you are not sample owner",
                                                  FORBIDDEN_FUNCTION_ACCESS_RESPONSE_CODE)
        return sample_restricted_func(*args, **kwargs)

    return wrapper
