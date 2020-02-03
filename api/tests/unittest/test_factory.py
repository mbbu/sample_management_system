from api import create_app
from api.config import TestConfig


def test_config():
    """Test create_app without passing test config"""
    assert not create_app().testing
    assert create_app(TestConfig.configs).testing


def test_home(client):
    response = client.get('/home')
    assert response.data == b'Hello, Welcome to M.B.B.U Sample Management System!'
