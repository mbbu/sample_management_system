from api.resources.base_resource import BaseResource
from flask_restful import Resource
from api.models.sample import Sample


class SampleResource (BaseResource):
    def get(self):
        samples = Sample.query.all()
        return jsonify({'samples' : samples})
