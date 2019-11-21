from flask import current_app
from flask_restful import reqparse, marshal, fields
from api.models.role import Role
from api.models.database import BaseModel
from api.resources.base_resource import BaseResource

class RoleResource(BaseResource):
    fields = {
        'code' : fields.String,
        'name' : fields.String,
        'description' : fields.String
    }

    def get(self):
        role = Role.query.all()
        data = marshal( role,self.fields)
        return BaseResource.send_json_message(data, 200)

    def post(self):
        args = RoleResource.role_parser()
        code = args['code']
        name = args['name']
        description = args['description']

        if not Role.role_exists(name):

            try:
                role = Role(code =code, name = name, description = description)
                BaseModel.db.session.add(role)
                BaseModel.db.session.commit()
                return BaseResource.send_json_message("Added Role Sucessfully", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding role", 500)
        current_app.logger.error("Error while adding role :> Duplicate records")
        return BaseResource.send_json_message("Role already exsists", 500)
    
    
    def put(self, id):
        args = RoleResource.role_parser()
        code = args['code']
        name = args['name']
        description = args['description']

        role = RoleResource.get_role(id)

        if role is not None:
            if code != role.code or name !=role.name or description !=role.description:

                try:
                    role.code =code
                    role.name = name
                    role.description = description

                    BaseModel.db.session.commit()
                    return BaseResource.send_json_message("Updated Role Sucessfully", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding role", 500)
        current_app.logger.error("Error while adding role :> Duplicate records")
        return BaseResource.send_json_message("Role already exsists", 500)

    def delete(self, id):
        role = RoleResource.get_role(id)

        if not role:
            return BaseResource.send_json_message("Role not found", 404)

        BaseModel.db.session.delete(role)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Role Deleted", 200)

    @staticmethod
    def role_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('code', required = True)
        parser.add_argument('name', required=True)
        parser.add_argument('description')

        args = parser.parse_args()
        return args

    @staticmethod
    def get_role(role_id):
        return BaseModel.db.session.query(Role).get(role_id)
