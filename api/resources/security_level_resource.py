from flask import current_app
from flask_restful import fields, marshal, reqparse

from api.models.security_level import SecurityLevel
from api.models.database import BaseModel
from api.resources.base_resource import BaseResource

class SecurityLevelResource (BaseResource):
    fields = {
        'code' : fields.String,
        'name' : fields.String,
        'description' : fields.String
    }
    def get(self):
        security_level = SecurityLevel.query.all()
        data = marshal(security_level, self.fields)
        # return output_json(data, 200)
        return BaseResource.send_json_message(data, 200)

    def post(self):
        args = SecurityLevelResource.security_level_parser()
        code = args['code']
        name = args['name']
        description = args['description']

        if not SecurityLevel.security_level_exists(code):
            try:
                security_level = SecurityLevel(code=code, name=name, description=description)
                BaseModel.db.session.add(security_level)
                BaseModel.db.session.commit()
                return BaseResource.send_json_message("Added new security level", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding security level", 500)
        current_app.logger.error("Error while adding security level :> Duplicate records")
        return BaseResource.send_json_message("Security level already exists")

    def put(self, code):
        args = SecurityLevelResource.security_level_parser()
        code = args['code']
        name = args['name']
        description = args['description']

        security_level = SecurityLevelResource.get_security_level(code)


        if security_level is not None:
            if  code != security_level.code or name !=security_level.name or \
                    code!= security_level.code or description !=security_level.description:
                try:
                    security_level.name = name
                    security_level.code = code
                    security_level.description = description

                    BaseModel.db.session.commit()
                    #current_app.logger.info("{0} updated some info; "
                                           # "name={0}, code={1}, description={2}"
                                            #.format(get_jwt_identity(), id, name, code, description, datetime.now()))
                    return BaseResource.send_json_message("Updated security level", 202)
                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating user. Another user has that email",
                                                          500)
            #else:
                #return BaseResource.send_json_message("No changes made", 304)
       # else:
            current_app.logger.error("Error while updating security level. Record does not exist.")
            return BaseResource.send_json_message("Security level already exists", 500)


    def delete(self, code):
        security_level = SecurityLevelResource.get_security_level(code)

        if security_level is None:
            return BaseResource.send_json_message("Security level not found", 404)

        BaseModel.db.session.delete(security_level)
        BaseModel.db.session.commit()
        #current_app.logger.info("{0} deleted {1}".format(get_jwt_identity(), security_level))
        return BaseResource.send_json_message("Security level Deleted", 200)

    @staticmethod
    def security_level_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('description')

        args = parser.parse_args()
        return args

    @staticmethod
    def get_security_level(code):
        return BaseModel.db.session.query(SecurityLevel).filter_by(code=code).first()










