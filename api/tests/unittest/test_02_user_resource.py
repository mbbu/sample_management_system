from flask import json, request
from flask_jwt_extended import create_access_token

from api import create_app as app

USER_DATA = {
    'first_name': 'ICIPE',
    'last_name': 'ADMIN',
    'email': 'admin@icipe.org',
    'role': '1',
    'password': 'Admin1sMa3str0'
}

with app().test_request_context():
    access_token = create_access_token(identity='admin@icipe.org')
headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}

"""
# ****************************
# ***                      ***
# ***  TEST GET REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_get_user(client):
    response = client.get('/users')
    assert b'message' in response.data
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Users not found'

    elif response.status_code == 200:
        # check that the list is more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; role, email and name(s)
        for item in range(len(data['message'])):
            assert data['message'][item]['email']
            assert data['message'][item]['first_name']
            assert data['message'][item]['last_name']
            assert data['message'][item]['role.name']


# todo: change the params to an admin user
def test_get_user_by_params(client):
    with app().test_request_context('/user?email=brittney71@gmail.com&deleted=false&role=8'):
        assert request.path == '/user'
        assert request.args['email'] == 'brittney71@gmail.com'
        assert request.args['deleted'] == 'false'
        assert request.args['role'] == '8'

    response = client.get('/user?email=brittney71@gmail.com&deleted=false&role=8')
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Users not found'

    elif response.status_code == 200:
        assert data['message']['email'] == 'brittney71@gmail.com'
        assert data['message']['first_name']
        assert data['message']['last_name']
        assert data['message']['role.name']


"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_user_with_half_info(client):
    response = client.post('/user', json={
        'first_name': 'ICIPE',
        'last_name': 'ADMIN',
        'email': 'admin@icipe.org',
        # 'role': '1',  <-- missing required parameter
        'password': 'Admin1sMa3str0'
    })

    assert response.status_code == 400


def test_create_user_with_all_info(client):
    response = client.post('/user', json=USER_DATA)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['message']['first_name'] and data['message']['first_name'] == 'ICIPE'
    assert data['message']['last_name'] and data['message']['last_name'] == 'ADMIN'
    assert data['message']['email'] and data['message']['email'] == 'admin@icipe.org'
    assert data['message']['role.name']
    assert data['message']['token']
    assert data['message']['refresh_token']
    assert data['message']['response'] and data['message']['response'] == 'Registered user'


def test_create_duplicate_user(client):
    response = client.post('/user', json=USER_DATA)
    data = json.loads(response.data)
    assert response.status_code == 409
    assert data['message'] == 'User already exists'


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_updating_user_without_jwt_token(client):
    response = client.put('/user', json=USER_DATA)
    assert response.status_code == 401


def test_updating_user_without_any_field_changes(client):
    response = client.put('/user', json=USER_DATA, headers=headers)
    assert response.status_code == 304


def test_updating_user_with_field_changes(client):
    response = client.put('/user', json={
        'first_name': 'I.C.I.P.E',
        'last_name': 'ADMIN',
        'email': 'admins@icipe.org',
        'role': '1',
        'password': 'Admin1sMa3str0'
    }, headers=headers)

    assert response.status_code == 202 or 409


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_user_without_jwt_token(client):
    response = client.delete('/user')
    assert response.status_code == 401


def test_deleting_another_user(client):
    with app().test_request_context():
        updated_access_token = create_access_token(identity='admin@icipe.org')
    updated_headers = {
        'Authorization': 'Bearer {}'.format(updated_access_token)
    }
    response = client.delete('/user', headers=updated_headers)
    assert response.status_code == 404


def test_deleting_user(client):
    with app().test_request_context():
        updated_access_token = create_access_token(identity='admins@icipe.org')
    updated_headers = {
        'Authorization': 'Bearer {}'.format(updated_access_token)
    }
    response = client.delete('/user', headers=updated_headers)
    assert response.status_code == 200 or 404

# todo: test if passwords are hashed
