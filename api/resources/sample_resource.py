from flask_restful import fields, marshal, marshal_with, output_json, reqparse
from api.models.sample import Sample
from api.resources.base_resource import BaseResource

post_parser = reqparse.RequestParser()

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
    

class SampleResource(BaseResource):
    fields = {
    'theme_id' : fields.Integer,
    'user_id': fields.Integer,
    'box_id' : fields.Integer,
    'animal_species': fields.String,
    'sample_type': fields.String,
    'sample_description': fields.String,
    'location_collected' : fields.String,
    'project': fields.String,
    'project_owner': fields.String,
    'retention_period': fields.Integer,
    'barcode': fields.String,
    'analysis': fields.String,
    'temperature': fields.String,
    'amount': fields.Integer
    }
  
    def get(self):
        samples = Sample.query.all()
        data = marshal(samples, self.fields)
        # return output_json(data, 200)
        return BaseResource.send_json_message(data, 200)

    
    def post(self):
        args = post_parser.parse_args()
        post_parser.add_argument('theme_id', type=str, location='json', required=False,  )
        post_parser.add_argument('user_id', type=str, location='json', required=False,  )
        post_parser.add_argument('box_id', type=str, location='json', required=False,  )
        post_parser.add_argument('animal_species', type=str, location='json', required=True,  )
        post_parser.add_argument('sample_type', type=str, location='json', required=True,  )
        post_parser.add_argument('sample_description', type=str, location='json', required=True,  )
        post_parser.add_argument('location_collected', type=str, location='json', required=True,  )
        post_parser.add_argument('project', type=str, location='json', required=True,  )
        post_parser.add_argument('project_owner', type=str, location='json', required=True,  )
        post_parser.add_argument('retention_period', type = int, location='json', required=True,  )
        post_parser.add_argument('barcode', type = int, location='json', required=True,  )
        post_parser.add_argument('temperature', type = int, location='json', required=True,  )
        post_parser.add_argument('amount', type = int, location='json', required=True,  )

        data = marshal(args, self.fields)
        return BaseResource.send_json_message(data, 200)

    def put(self):
        

    
