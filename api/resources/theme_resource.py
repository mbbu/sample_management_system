from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, fields, marshal

from api.models.database import BaseModel
from api.models.theme import Theme
from api.resources.base_resource import BaseResource
from api.resources.decorators.user_role_decorators import is_sys_admin
from api.search.search import add_to_index, remove_from_index
from api.utils import log_duplicate, log_304, format_and_lower_str, has_required_request_params, log_create, log_update, \
    standard_non_empty_string, non_empty_string, get_query_params


class ThemeResource(BaseResource):
    fields = {
        'code': fields.String,
        'name': fields.String
    }

    def get(self):
        Theme.reindex()

        query_strings = get_query_params()
        if query_strings is not None:
            for query_string in query_strings:
                query, total = Theme.search(query_string, 1, 15)
                themes = query.all()

                data = marshal(themes, self.fields)
                return BaseResource.send_json_message(data, 200)

        else:
            themes = Theme.query.all()
            if themes is None:
                return BaseResource.send_json_message("Themes not found", 404)
            else:
                data = marshal(themes, self.fields)
                return BaseResource.send_json_message(data, 200)

    @jwt_required
    @is_sys_admin
    def post(self):
        args = ThemeResource.theme_parser()
        code = args['code']
        name = args['name']

        if not Theme.theme_exists(code):
            try:
                theme = Theme(code=code, name=name)
                BaseModel.db.session.add(theme)
                BaseModel.db.session.commit()
                add_to_index(Theme.index_name, theme)
                log_create(theme)
                return BaseResource.send_json_message("Theme successfully created", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding theme", 500)
        log_duplicate(Theme.query.filter(Theme.code == code).first())
        return BaseResource.send_json_message("Theme already exists", 409)

    @jwt_required
    @is_sys_admin
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers.get('code'))

        theme = ThemeResource.get_theme(code)
        if theme is not None:
            args = ThemeResource.theme_parser()
            name = args['name']
            code = args['code']

            if name != theme.name or code != theme.code:
                old_info = str(theme)
                try:
                    theme.code = code
                    theme.name = name
                    BaseModel.db.session.commit()
                    add_to_index(Theme.index_name, theme)
                    log_update(old_info, theme)
                    return BaseResource.send_json_message("Theme successfully updated", 200)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating theme. Another theme has that name or "
                                                          "code", 500)
            log_304(theme)
            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("Theme not found", 404)

    @jwt_required
    @is_sys_admin
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers.get('code'))
        theme = ThemeResource.get_theme(code)

        if not theme:
            return BaseResource.send_json_message("Theme not found", 404)

        BaseModel.db.session.delete(theme)
        BaseModel.db.session.commit()
        remove_from_index(Theme.index_name, theme)
        return BaseResource.send_json_message("Theme deleted", 200)

    @staticmethod
    def theme_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, type=non_empty_string)
        parser.add_argument('code', required=True, type=standard_non_empty_string)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_theme(code):
        return BaseModel.db.session.query(Theme).filter_by(code=code).first()
