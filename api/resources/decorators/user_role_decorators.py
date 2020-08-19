"""
    These decorator functions check the user role and return true or false appropriately

"""
from flask import request
from flask_jwt_extended import get_jwt_identity

from api import BaseResource
from api.constants import SYSADMIN, FORBIDDEN_FUNCTION_ACCESS_RESPONSE, FORBIDDEN_FUNCTION_ACCESS_RESPONSE_CODE, \
    THEMEADMIN
from api.models import User, Sample, Role, Publication
from api.utils import get_user_by_email


def is_sys_admin(admin_restricted_func):
    """
    Decorator func to check if the user is the admin before executing a function
    :param admin_restricted_func:
    :return:
    """

    def wrapper(*args, **kwargs):
        user = get_user_by_email(get_jwt_identity())

        admin = User.query.filter(User.id == user.id, user.role.code == SYSADMIN).first()
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
        user = get_user_by_email(get_jwt_identity())

        theme_admin = User.query.filter(User.id == user.id, user.role.code == THEMEADMIN).first()
        sys_admin = User.query.filter(User.id == user.id, user.role.code == SYSADMIN).first()
        if not theme_admin and not sys_admin:
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
        user = get_user_by_email(get_jwt_identity())

        # check if they are sample owners
        user_samples = Sample.query.filter(Sample.user_id == user.id).all()
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
        sys_admin = User.query.filter(User.id == user.id, user.role.code == SYSADMIN).first()
        theme_admin = User.query.filter(User.id == user.id, user.role.code == THEMEADMIN).first()

        if not sample_owner and theme_admin is None and sys_admin is None:
            return BaseResource.send_json_message("Cannot access this function, you are not the sample owner",
                                                  FORBIDDEN_FUNCTION_ACCESS_RESPONSE_CODE)
        return sample_restricted_func(*args, **kwargs)

    return wrapper


def authorized_to_modify_user(deactivate_user_restricted_function):
    """
    Decorator func to check if the user is the admin allowing them to deactivate other user accounts
    :param deactivate_user_restricted_function:
    :return:
    """

    def wrapper(*args, **kwargs):
        # check if user requesting deactivation is in their account or is the system admin
        user = get_user_by_email(get_jwt_identity())
        admin = User.query.join(Role).filter(User.id == user.id, Role.code == SYSADMIN).first()

        if (get_jwt_identity() != user.email) and not admin:
            return BaseResource.send_json_message("You cannot delete another user!",
                                                  FORBIDDEN_FUNCTION_ACCESS_RESPONSE_CODE)
        return deactivate_user_restricted_function(*args, **kwargs)

    return wrapper


def is_publication_owner(publication_restricted_func):
    """
    Decorator func to check if the user is the admin before executing a function
    :param publication_restricted_func:
    :return:
    """

    def wrapper(*args, **kwargs):
        user = get_user_by_email(get_jwt_identity())

        # check if they are publication owners
        user_publications = Publication.query.filter(Publication.user_id == user.id).all()
        this_pub_title = request.headers['title']
        publication_owner = False

        for publication in user_publications:
            if publication.publication_title == this_pub_title:
                publication_owner = True
                break
            else:
                publication_owner = False
                continue

        # check if they are either a system admin or theme admin
        sys_admin = User.query.filter(User.id == user.id, user.role.code == SYSADMIN).first()
        theme_admin = User.query.filter(User.id == user.id, user.role.code == THEMEADMIN).first()

        if not publication_owner and theme_admin is None and sys_admin is None:
            return BaseResource.send_json_message("Cannot access this function, you are not the publication owner",
                                                  FORBIDDEN_FUNCTION_ACCESS_RESPONSE_CODE)
        return publication_restricted_func(*args, **kwargs)

    return wrapper
