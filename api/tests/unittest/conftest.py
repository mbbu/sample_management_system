import os
import tempfile

import pytest

from api import create_app
from api.models.database import BaseModel


@pytest.fixture
def app():
    """create and configure a new app instance for each test"""
    db_fd, db_path = tempfile.mkstemp()  # create a temporary file to isolate the database for each test
    app = create_app({"TESTING": True, "DATABASE": db_path})  # create the app with common test config

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
