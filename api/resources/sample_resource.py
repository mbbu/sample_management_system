from flask_restful import fields, marshal, output_json

from api.models.sample import Sample
from api.resources.base_resource import BaseResource


class SampleResource(BaseResource):
    """
        Checkout how the resource is built;
            the fields represent the actual database fields,
            the get request uses the *marshal()* and *output_json()* methods to;
                1. Marshal the object fetched from the database with the fields
                2. Output the marshaled data as a JSON object + the HTTP status code.
                NB: output_json() is optional, best case is to use *BaseResource.send_json_message()*
                Checkout below at how the two have been used, one is commented out.

            For Post and Put methods;
                after computation, we use the BaseResource.send_json_message() method to update the client on the status
                of the operation.
    """
    fields = {
        'user_id': fields.Integer,
        'animal_species': fields.String,
        'sample_type': fields.String,
        'sample_description': fields.String,
        'project': fields.String,
        'barcode': fields.String,
        'box_id': fields.Integer,
        'retention_period': fields.Integer,
        'amount': fields.Integer
    }

    def get(self):
        samples = Sample.query.all()
        data = marshal(samples, self.fields)
        # return output_json(data, 200)
        return BaseResource.send_json_message(data, 200)
