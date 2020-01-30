import os
import tempfile

import pytest

from api import create_app
from api.models.database import BaseModel


db_fd, db_path = tempfile.mkstemp()  # create a temporary file to isolate the database for each test
basedir = os.path.abspath(os.path.dirname(__file__))
configs = {"TESTING": True,
           "DATABASE": db_path,
           'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + os.path.join(basedir, 'test.db'),
           'SQLALCHEMY_TRACK_MODIFICATIONS': False}


@pytest.fixture
def app():
    """create and configure a new app instance for each test"""
    # create the app with common test config
    app = create_app(configs)

    with app.app_context():
        BaseModel.init_app(app)
    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
