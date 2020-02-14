from flask import current_app
from flask_jwt_extended import jwt_required
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

    # @jwt_required
    def post(self):
        args = ThemeResource.theme_parser()
        code = args['code']
        name = args['name']

        if not Theme.theme_exists(name):
            try:
                theme = Theme(code=code, name=name)
                BaseModel.db.session.add(theme)
                BaseModel.db.session.commit()
                return BaseResource.send_json_message("Added new theme", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding theme", 500)
        current_app.logger.error("Error while adding theme :> Duplicate records")
        return BaseResource.send_json_message("Theme already exists", 500)

    @jwt_required
    def put(self):
        args = ThemeResource.theme_parser()
        name = args['name']
        code = args['code']

        theme = ThemeResource.get_theme(code)

        if theme is not None:
            if name != theme.name or code != theme.code:
                try:
                    theme.code = code
                    theme.name = name
                    BaseModel.db.session.commit()
                    return BaseResource.send_json_message("Updated theme", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding theme. Another theme has that name or "
                                                          "code", 500)

            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("Theme not found", 404)

    @jwt_required
    def delete(self, code):
        theme = ThemeResource.get_theme(code)

        if not theme:
            return BaseResource.send_json_message("Theme not found", 404)

        BaseModel.db.session.delete(theme)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Theme deleted", 200)

    @staticmethod
    def theme_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('code')

        args = parser.parse_args()
        return args

    @staticmethod
    def get_theme(theme_code):
        return BaseModel.db.session.query(Theme).get(theme_code)
