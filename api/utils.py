from api.models.database import BaseModel
from api.models.user import User


def get_user(email):
    return BaseModel.db.session.query(User).filter_by(email=email).first()


def non_empty_string(s: str):
    if not s:
        raise ValueError("Expected a non empty string")
    return s


def non_empty_int(i: int):
    if not i:
        raise ValueError("Expected an integer")
    return i