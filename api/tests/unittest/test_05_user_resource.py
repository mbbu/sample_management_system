from flask import json
from flask_jwt_extended import create_access_token

from api import create_app as app
from api.tests.unittest.utils_for_tests import headers, USER_DATA, create_role, create_user, prepare_user_test, \
    user_resource_route

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_user_with_half_info(client):
    response = client.post(user_resource_route, json={
        'first_name': 'ICIPE',
        'last_name': 'ADMIN',
        'email': 'admin@icipe.org',
        # 'role': '1',  <-- missing required parameter
        'password': 'Admin1sMa3str0'
    })

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['message'] == {'role': 'Missing required parameter in the JSON body or the post body or the query '
                                       'string'}


def test_create_user_with_all_info(client):
    create_role(client)
    response = create_user(client)
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
    prepare_user_test(client)
    response = create_user(client)
    data = json.loads(response.data)
    assert response.status_code == 409
    assert data['message'] == 'User already exists'


"""
# # ****************************
# # ***                      ***
# # ***  TEST GET REQUESTS   ***
# # ***                      ***
# # ****************************
"""


def test_get_user(client):
    prepare_user_test(client)
    response = client.get(user_resource_route)
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


def test_get_user_by_params(client):
    prepare_user_test(client)
    response = client.get(user_resource_route, headers=headers)
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'User not found'

    elif response.status_code == 200:
        assert data['message']['email']
        assert data['message']['first_name']
        assert data['message']['last_name']
        assert data['message']['role.name']


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_updating_user_without_jwt_token(client):
    response = client.put(user_resource_route, json=USER_DATA)
    assert response.status_code == 401


def test_updating_user_without_any_field_changes(client):
    prepare_user_test(client)
    response = client.put(user_resource_route, json=USER_DATA, headers=headers)
    assert response.status_code == 304


def test_updating_user_with_field_changes(client):
    prepare_user_test(client)
    response = client.put(user_resource_route, json={
        'first_name': 'I.C.I.P.E',
        'last_name': 'ADMIN',
        'email': 'admins@icipe.org',
        'role': '1',
        'password': 'Admin1sMa3str0'
    }, headers=headers)

    assert response.status_code == 202


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_user_without_jwt_token(client):
    response = client.delete(user_resource_route)
    assert response.status_code == 401


def test_deleting_another_user(client):
    with app().test_request_context():
        updated_access_token = create_access_token(identity='admin@icipe.org')
    updated_headers = {
        'Authorization': 'Bearer {}'.format(updated_access_token)
    }
    response = client.delete(user_resource_route, headers=updated_headers)
    assert response.status_code == 404


def test_deleting_user(client):
    prepare_user_test(client)
    response = client.delete(user_resource_route, headers=headers)
    assert response.status_code == 200

# todo: test if passwords are hashed
