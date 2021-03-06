from flask import json, request

from api import create_app as app
from api.tests.unittest.utils_for_tests import role_data, headers, create_role, role_resource_route

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_role_by_non_logged_in_user(client):
    response = client.post(role_resource_route, json=role_data)
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data['msg'] == 'Missing Authorization Header'


def test_create_role(client):
    response = create_role(client)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['message'] == 'Added Role Successfully'


def test_create_duplicate_role(client):
    create_role(client)  # 1st role created
    response = client.post(role_resource_route, json=role_data, headers=headers)  # duplicate of 1st role
    data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Role already exists'


def test_create_role_without_required_info(client):
    response = client.post(role_resource_route, json={
        'code': '001',
        # 'name': 'Admin', <-- missing required info.
        'description': 'In Charge of the system'
    }, headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == {'name': 'Missing required parameter in the JSON body or the post body or the query '
                                       'string'}


"""
# ****************************
# ***                      ***
# ***  TEST GET REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_get_role(client):
    create_role(client)
    response = client.get('/roles')
    data = json.loads(response.data)

    if response.status_code == 200:
        # check that the list has more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; code, name and description
        for item in range(len(data['message'])):
            assert data['message'][item]['code']
            assert data['message'][item]['name']
            assert data['message'][item]['description']


def test_get_role_by_params(client):
    with app().test_request_context(role_resource_route):
        assert request.path == role_resource_route

    create_role(client)
    response = client.get(role_resource_route, headers=headers)
    data = json.loads(response.data)

    if response.status_code == 200:
        assert data['message']['code'] == 'admin1'
        assert data['message']['name'] == 'Admin'
        assert data['message']['description'] == 'In Charge of the system'


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_updating_role_without_jwt_token(client):
    response = client.put(role_resource_route, json=role_data)
    assert response.status_code == 401


def test_updating_non_existent_role(client):
    response = client.put(role_resource_route, json=role_data, headers=headers)
    assert response.status_code == 404


def test_updating_role_without_any_field_changes(client):
    create_role(client)
    response = client.put(role_resource_route, json=role_data, headers=headers)
    assert response.status_code == 304


def test_updating_role_with_field_changes(client):
    create_role(client)
    response = client.put('/user', json={
        'code': '100',
        'name': 'Admin',
        'description': 'In Charge of the system'
    }, headers=headers)

    assert response.status_code == 202 or 409


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_role_without_jwt_token(client):
    response = client.delete(role_resource_route)
    assert response.status_code == 401


def test_deleting_role(client):
    response = client.delete(role_resource_route, headers=headers)
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Role not found'

    elif response.status_code == 200:
        assert data['message'] == 'Role deleted'
