import os
import sqlite3
import tempfile
from sqlite3 import Error

import pytest
from flask import current_app

from api import create_app
from api.config import TestConfig


@pytest.fixture
def app():
    """create and configure a new app instance for each test"""
    # create the app with common test config
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_fd, db_name = tempfile.mkstemp(dir=base_dir, suffix='.db')

    app = create_app(TestConfig.configs)
    TestConfig.configs.update({'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_name})

    with app.app_context():
        create_database(db_name)
    yield app
    os.close(db_fd)
    os.unlink(db_fd)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


def create_database(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)

        with current_app.open_resource("./models/schema/schema.sql", 'rb') as f:
            conn.executescript(f.read().decode("utf8"))
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
