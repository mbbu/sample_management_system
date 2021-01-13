from flask_restful import Resource
from flask_restful.representations.json import output_json


class BaseResource(Resource):

    @staticmethod
    def send_json_message(message, code):
        return output_json({"message": message}, code)
