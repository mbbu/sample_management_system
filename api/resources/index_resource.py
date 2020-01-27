from api.resources.base_resource import BaseResource


class IndexResource(BaseResource):
    def get(self):
        return BaseResource.send_json_message('Hello, Welcome to M.B.B.U Sample Management System!', 200)
