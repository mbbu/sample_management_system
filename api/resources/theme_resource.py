from flask import current_app
from flask_restful import reqparse, fields
from api.models.database import BaseModel
from api.models.theme import Theme
from api.resources.base_resource import BaseResource


class ThemeResource(BaseResource):
    fields = {
        'name': fields.String
    }

    def get(self):
        return BaseResource.send_json_message("themes", 200)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)

        args = parser.parse_args()
        name = args['name']

        try:
            theme = Theme(name=name)
            BaseModel.db.session.add(theme)
            BaseModel.db.session.commit()
            return BaseResource.send_json_message("Added new theme", 202)

        except Exception as e:
            BaseModel.db.session.rollback()
            current_app.logger.error(e)
            return BaseResource.send_json_message("Error while adding theme", 500)
