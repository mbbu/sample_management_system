from flask_restful import fields, marshal, output_json, reqparse
from flask import current_app
from api.models.sample import Sample
from api.resources.base_resource import BaseResource
from api.models.database import BaseModel

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
        args = SampleResource.sample_parser()
        theme_id = args['theme_id']
        user_id = args['user_id']
        box_id = args['box_id']
        animal_species = args['animal_species']
        sample_type = args['sample_type']
        sample_description = args['sample_description']
        location_collected = args['location_collected'] 
        project = args['project']
        project_owner = args['project_owner']
        retention_period = args['retention_period']
        barcode =  args['barcode']
        analysis = args['analysis']
        temperature = args['temperature']
        amount = args['amount']

        sample = Sample( theme_id= theme_id, user_id =user_id, box_id = box_id, animal_species = animal_species, sample_type= sample_type,
                        sample_description = sample_description, location_collected= location_collected, project =project, project_owner = project_owner,
                        retention_period = retention_period, barcode=barcode, analysis=analysis, temperature = temperature, amount=amount)
        
        BaseModel.db.session.add(sample)
        BaseModel.db.session.commit()
        return BaseResource.send_json_message("Updated the Sample", 200)

    def put(self, id):
        args = SampleResource.sample_parser()
        theme_id = args['theme_id']
        user_id = args['user_id']
        box_id = args['box_id']
        animal_species = args['animal_species']
        sample_type = args['sample_type']
        sample_description = args['sample_description']
        location_collected = args['location_collected'] 
        project = args['project']
        project_owner = args['project_owner']
        retention_period = args['retention_period']
        barcode =  args['barcode']
        analysis = args['analysis']
        temperature = args['temperature']
        amount = args['amount']

        sample = SampleResource.get_sample(id)

        if Sample is not None:
            if theme_id != theme_id or user_id != sample.user_id or box_id != sample.box_id or animal_species != sample.animal_species or sample_type != sample.sample_type or sample_description != sample.sample_description or location_collected != sample.location_collected or  project != sample.project or project_owner != sample.project_owner or retention_period != sample.retention_period or barcode != sample.barcode or analysis != sample.analysis or temperature != sample.temperature or amount != sample.amount :
                try:
                    theme_id= theme_id
                    user_id =user_id
                    box_id = box_id 
                    animal_species =animal_species 
                    sample_type= sample_type
                    sample_description = sample_description 
                    location_collected= location_collected 
                    project =project
                    project_owner = project_owner
                    retention_period = retention_period
                    barcode=barcode
                    analysis=analysis
                    temperature = temperature
                    amount=amount
            
                    BaseModel.db.session.commit()
                    return BaseResource.send_json_message("Updated the Sample", 200)
                
                except Exception as e:
                    current_app.logger.error(e)
                    BaseModel.db.session.rollback()
                    return BaseResource.send_json_message("Error while adding sample. Another sample has that name or "
                                                          "code", 500)

            return BaseResource.send_json_message("No changes made", 304)
        return BaseResource.send_json_message("Sample not found", 404)

    def delete(self, id):

        sample = SampleResource.get_sample(id)

        if not sample:
            return BaseResource.send_json_message("Sample not found", 404)

        BaseModel.db.session.delete(sample)
        BaseModel.db.session.commit()

        return BaseResource.send_json_message("Sample Sucessfully deleted", 200)


    @staticmethod
    def sample_parser():
        parser = reqparse.RequestParser()
        parser.add_argument('theme_id', required=False )
        parser.add_argument('user_id', required=False )
        parser.add_argument('box_id', required=False )
        parser.add_argument('animal_species', required=True)
        parser.add_argument('sample_type', required=True)
        parser.add_argument('sample_description', required=True)
        parser.add_argument('location_collected', required=True)
        parser.add_argument('project', required=True)
        parser.add_argument('project_owner',  required=True)
        parser.add_argument('retention_period',  required=True)
        parser.add_argument('barcode', required=True)
        parser.add_argument('analysis', required=True)
        parser.add_argument('temperature', required=True)
        parser.add_argument('amount',  required=True)

        args = parser.parse_args()
        return args

    @staticmethod
    def get_sample(sample_id):
        return BaseModel.db.session.query(Sample).get(sample_id)
        