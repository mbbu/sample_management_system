from flask import  current_app
from flask_user import login_required,roles_required
from flask_jwt_extended import current_user
from flask_restful import fields, reqparse, marshal
from functools import wraps

from api.resources.auth_resource import BaseResource

class RoleAuthResource(BaseResource):
    fields = {
        'code ': fields.String,
        'name': fields.String
    }

@roles_required('ANY')
def login_required() :
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
                return  current_app.login_manageer.unauthorized()
            if ((current_user.role != role) and (role != "ANY")):
                return current_app.login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
