from flask_login import current_user
from flask_restful import fields
from flask_principal import identity_loaded, RoleNeed, UserNeed

from api.resources.base_resource import BaseResource

class RoleAuthResource(BaseResource):
    fields = {
        'name': fields.String,
        'code': fields.String
    }

    def on_identity_loaded(sender, identity_loaded):
        identity_loaded.user = current_user

    if hasattr(current_user, 'id'):
        identity_loaded.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity_loaded.provides.add(RoleNeed(role.code))


