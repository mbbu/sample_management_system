from flask import request

from api.models import *
from api.resources.base_resource import BaseResource
from api.utils import format_and_lower_str, faker


class FakeDataResource(BaseResource):
    def post(self):
        count = int(request.args.get('count'))
        model = format_and_lower_str(request.args.get('model'))

        if model == 'box':
            db_model = Box
            return faker(count, db_model, model)
        elif model == 'chamber':
            db_model = Chamber
            return faker(count, db_model, model)
        elif model == 'freezer':
            db_model = Freezer
            return faker(count, db_model, model)
        elif model == 'lab' or model == 'laboratory':
            db_model = Laboratory
            return faker(count, db_model, model)
        elif model == 'publication':
            db_model = Publication
            return faker(count, db_model, model)
        elif model == 'quantity type':
            db_model = QuantityType
            return faker(count, db_model, model)
        elif model == 'rack':
            db_model = Rack
            return faker(count, db_model, model)
        elif model == 'role':
            db_model = Role
            return faker(count, db_model, model)
        elif model == 'sample':
            db_model = Sample
            return faker(count, db_model, model)
        elif model == 'biohazard level':
            db_model = BioHazardLevel
            return faker(count, db_model, model)
        elif model == 'theme':
            db_model = Theme
            return faker(count, db_model, model)
        elif model == 'tray':
            db_model = Tray
            return faker(count, db_model, model)
        elif model == 'user':
            db_model = User
            return faker(count, db_model, model)
        else:
            return
