import pytest

from api import create_app
from api.config import TestConfig
from api.models.database import BaseModel


@pytest.fixture
def app():
    """create and configure a new app instance for each test"""
    # create the app with common test config
    app = create_app(TestConfig.configs)

    with app.app_context():
        BaseModel.init_app(app)
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()
