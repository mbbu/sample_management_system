from flask import json

from api.tests.unittest.test_02_user_resource import prepare_user_test

login_details = {
    'email': 'admin@icipe.org',
    'password': 'Admin1sMa3str0'
}


def test_login(client):
    prepare_user_test(client)
    response = client.post('/auth', json=login_details)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message']['first_name'] and data['message']['first_name'] == 'ICIPE'
    assert data['message']['last_name'] and data['message']['last_name'] == 'ADMIN'
    assert data['message']['email'] and data['message']['email'] == 'admin@icipe.org'
    assert data['message']['token']
    assert data['message']['refresh_token']
