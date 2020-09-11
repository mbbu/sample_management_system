from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import reqparse, marshal, fields

from api.models.database import BaseModel
from api.models.project import Project
from api.resources.base_resource import BaseResource
from api.resources.theme_resource import ThemeResource
from api.utils import format_and_lower_str, log_create, log_duplicate, \
    log_update, log_delete, has_required_request_params, standard_non_empty_string, log_304, get_user_by_email


class ProjectResource(BaseResource):
    fields = {
        'code': fields.String,
        'theme.name': fields.String,
        'description': fields.String,
        'name': fields.String,
        'lead.first_name': fields.String,
        'lead.last_name': fields.String,
        'lead.email': fields.String
    }

    def get(self):
        if request.headers.get('code') is not None:
            code = format_and_lower_str(request.headers['code'])
            project = ProjectResource.get_project(code)
            data = marshal(project, self.fields)
            return BaseResource.send_json_message(data, 200)
        else:
            projects = Project.query.all()
            data = marshal(projects, self.fields)
            return BaseResource.send_json_message(data, 200)

    @jwt_required
    # @is_sys_admin
    def post(self):
        args = ProjectResource.project_parser()
        code = args['code']
        theme = ThemeResource.get_theme(args['theme']).id
        name = args['name']
        head = get_user_by_email(args['head']).id
        description = args['description']

        if not Project.project_exists(code):
            try:
                project = Project(code=code, theme_id=theme, name=name, head=head,
                                  description=description)
                BaseModel.db.session.add(project)
                BaseModel.db.session.commit()
                log_create(project)
                return BaseResource.send_json_message("Added Project Successfully", 201)

            except Exception as e:
                current_app.logger.error(e)
                BaseModel.db.session.rollback()
                return BaseResource.send_json_message("Error while adding project", 500)
        log_duplicate(Project.query.filter(Project.code == code).first())
        return BaseResource.send_json_message("Project already exists", 409)

    @jwt_required
    # @is_sys_admin
    @has_required_request_params
    def put(self):
        code = format_and_lower_str(request.headers['code'])
        project = ProjectResource.get_project(code)

        if project is None:
            return BaseResource.send_json_message("Project not found", 404)

        else:
            args = ProjectResource.project_parser()
            project_code = args['code']
            theme = ThemeResource.get_theme(args['theme']).id
            description = args['description']
            name = args['name']
            head = get_user_by_email(args['head']).id

            if project_code != project.code or theme != project.theme_id or name != project.name or \
                    head != project.head or description != project.description:
                old_info = str(project)
                try:
                    project.code = project_code
                    project.theme_id = theme
                    project.description = description
                    project.name = name
                    project.head = head
                    BaseModel.db.session.commit()
                    log_update(old_info, project)
                    return BaseResource.send_json_message("Updated Project Successfully", 202)

                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while updating project", 500)
            log_304(project)
            return BaseResource.send_json_message("No changes made", 304)

    @jwt_required
    # @is_sys_admin
    @has_required_request_params
    def delete(self):
        code = format_and_lower_str(request.headers['code'])
        project = ProjectResource.get_project(code)

        if not project:
            return BaseResource.send_json_message("Project not found", 404)

        BaseModel.db.session.delete(project)
        BaseModel.db.session.commit()
        log_delete(project)
        return BaseResource.send_json_message("Project deleted", 200)

    @staticmethod
    def project_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True, type=standard_non_empty_string)
        parser.add_argument('theme', required=True)
        parser.add_argument('description')
        parser.add_argument('name')
        parser.add_argument('head')

        args = parser.parse_args()
        return args

    @staticmethod
    def get_project(code):
        return BaseModel.db.session.query(Project).filter_by(code=code).first()
