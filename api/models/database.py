from api import db


class BaseModel(object):
    db = db

    @staticmethod
    def migrate_db():
        from api.models.role import Role
        from api.models.sample import Sample
        from api.models.theme import Theme
        from api.models.user import User
        from api.models.box import Box
        from api.models.tray import Tray
        from api.models.rack import Rack
        from api.models.chamber import Chamber
        from api.models.freezer import Freezer
        from api.models.laboratory import Laboratory
        from api.models.publication import Publication
        from api.models.quantity_type import QuantityType
        from api.models.project import Project
        from api.models.sample_request import SampleRequest
        from api.models.slot import Slot
        from api.models.housedata import AnimalHealthHouseData
        from api.models.study_block import StudyBlock
        return [
            Role, User, Theme, Sample, Slot, StudyBlock,
            Box, Tray, Rack, QuantityType, Chamber, SampleRequest,
            Freezer, Laboratory, Publication, Project, AnimalHealthHouseData
        ]
