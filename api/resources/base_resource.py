from flask_restful import Resource
from flask_restful.representations.json import output_json


class BaseResource(Resource):

    @staticmethod
    def send_json_message(message, code):
        headers = {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                   'Access-Control-Allow-Methods': 'OPTIONS, HEAD, GET, POST, DELETE, PUT'}
        return output_json({"message": message}, code, headers=headers)
