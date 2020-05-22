"""
    These decorator functions check the user role and return true or false appropriately

"""
from flask_jwt_extended import get_jwt_identity

from api import BaseResource
from api.constants import SYSADMIN, FORBIDDEN_FUNCTION_ACCESS_RESPONSE, FORBIDDEN_FUNCTION_ACCESS_RESPONSE_CODE, \
    THEMEADMIN
from api.models import User


def is_sys_admin(admin_restricted_func):
    """
    Decorator func to check if the user is the admin before executing a function
    :param admin_restricted_func:
    :return:
    """

    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        admin = User.query.filter(User.id == user_id, User.role_id == SYSADMIN).first()
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
        user_id = get_jwt_identity()
        theme_admin = User.query.filter(User.id == user_id, User.role_id == THEMEADMIN).first()
        if not theme_admin:
            return BaseResource.send_json_message(FORBIDDEN_FUNCTION_ACCESS_RESPONSE,
                                                  FORBIDDEN_FUNCTION_ACCESS_RESPONSE_CODE)
        return theme_admin_restricted_func(*args, **kwargs)

    return wrapper
