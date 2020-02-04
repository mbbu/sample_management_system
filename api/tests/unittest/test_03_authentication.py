from flask import json

login_details = {
    'email': 'admins@icipe.org',
    'password': 'Admin1sMa3str0'
}


def test_login(client):
    response = client.post('/auth', json=login_details)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message']['first_name'] and data['message']['first_name'] == 'I.C.I.P.E'
    assert data['message']['last_name'] and data['message']['last_name'] == 'ADMIN'
    assert data['message']['email'] and data['message']['email'] == 'admins@icipe.org'
    assert data['message']['token']
    assert data['message']['refresh_token']
