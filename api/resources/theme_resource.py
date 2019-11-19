from flask import current_app
from flask_restful import reqparse, fields, marshal

from api.models.database import BaseModel
from api.models.theme import Theme
from api.resources.base_resource import BaseResource


class ThemeResource(BaseResource):
    fields = {
        'code': fields.String,
        'name': fields.String
    }

    def get(self):
        themes = Theme.query.all()
        data = marshal(themes, self.fields)
        return BaseResource.send_json_message(data, 200)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code')
        parser.add_argument('name', required=True)

        args = parser.parse_args()
        code = args['code']
        name = args['name']

        if not Theme.theme_exists(name):
            try:
                theme = Theme(name=name)
                BaseModel.db.session.add(theme)
                BaseModel.db.session.commit()
                return BaseResource.send_json_message("Added new theme", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding theme", 500)
        current_app.logger.error("Error while adding theme :> Duplicate records")
        return BaseResource.send_json_message("Theme already exists", 500)

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('code')

        args = parser.parse_args()
        name = args['name']
        code = args['code']

        theme = BaseModel.db.session.query(Theme).get(id)

        if name != theme.name:
            if Theme.theme_exists(name):
                current_app.logger.error("Error while adding theme :> Duplicate records")
                return BaseResource.send_json_message("Theme already exists", 500)

            try:
                theme.code = code
                theme.name = name
                BaseModel.db.session.commit()
                return BaseResource.send_json_message("Updated theme", 202)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding theme", 500)
        return BaseResource.send_json_message("No changes made", 200)
