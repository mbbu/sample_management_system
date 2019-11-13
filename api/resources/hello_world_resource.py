from api.resources.base_resource import BaseResource


class HelloWorldResource(BaseResource):
    def get(self):
        return BaseResource.send_json_message('Hello, Welcome to MBBU Sample Management System!', 200)
