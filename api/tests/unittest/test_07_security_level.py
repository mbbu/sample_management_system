from flask import json

from api.tests.unittest.utils_for_tests import security_level_data, create_security_level, security_level_headers, \
    security_level_code, security_level_updated_data, access_token, security_level_resource_route

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_security_level_by_non_logged_in_user(client):
    response = client.post(security_level_resource_route, json=security_level_data)
    assert response.status_code == 401


def test_create_security_level(client):
    response = create_security_level(client)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['message'] == "Security level successfully created"


def test_create_security_level_with_missing_info(client):
    response = client.post(security_level_resource_route, json={
        # 'name': 'Ebola',  <-- missing required param
        'code': security_level_code,
        'description': 'CDC L1'
    }, headers=security_level_headers)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == {'name': 'Missing required parameter in the JSON body or the post body or the query '
                                       'string'}


def test_create_duplicate_security_level(client):
    create_security_level(client)
    response = create_security_level(client)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Security level already exists'


"""
# ****************************
# ***                      ***
# ***  TEST GET REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_get_non_existing_security_level(client):
    response = client.get(security_level_resource_route, headers={'code': 'security_level_code'})
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Security level not found'


def test_get_security_level(client):
    create_security_level(client)
    response = client.get(security_level_resource_route)
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Security levels not found'

    elif response.status_code == 200:
        # check that the list is more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; freezer, type and code
        for item in range(len(data['message'])):
            assert data['message'][item]['code'] == 'a1'
            assert data['message'][item]['name'] == 'Ebola'
            assert data['message'][item]['description'] == 'CDC L1'


def test_get_security_level_by_param(client):
    create_security_level(client)
    response = client.get(security_level_resource_route, headers=security_level_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message']['code'] == 'a1'
    assert data['message']['name'] == 'Ebola'
    assert data['message']['description'] == 'CDC L1'


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_update_security_level_by_non_logged_in_user(client):
    response = client.put(security_level_resource_route, json=security_level_updated_data)
    assert response.status_code == 401


def test_update_security_level(client):
    create_security_level(client)
    response = client.put(security_level_resource_route, json=security_level_updated_data,
                          headers=security_level_headers)
    data = json.loads(response.data)

    assert response.status_code == 202
    assert data['message'] == 'Security level successfully updated'


def test_updating_security_level_without_any_field_changes(client):
    create_security_level(client)
    response = client.put(security_level_resource_route, json=security_level_data, headers=security_level_headers)
    print(response.data)
    assert response.status_code == 304


def test_update_non_existing_security_level(client):
    create_security_level(client)
    response = client.put(security_level_resource_route, json=security_level_headers, headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'code': 'security_level_code'  # <-- wrong/non-existing code
    })
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Security level not found'


def test_update_security_level_without_identity(client):
    create_security_level(client)
    response = client.put(security_level_resource_route, json=security_level_updated_data, headers={
        'Authorization': 'Bearer {}'.format(access_token)  # <-- missing security_level code in header
    })
    assert response.status_code == 400


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_security_level_by_non_logged_in_user(client):
    response = client.delete(security_level_resource_route)
    assert response.status_code == 401


def test_deleting_security_level_without_identity(client):
    response = client.delete(security_level_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token)})
    assert response.status_code == 400


def test_deleting_non_existent_security_level(client):
    create_security_level(client)
    response = client.delete(security_level_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token),
                                                                     'code': '123'})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data['message'] == 'Security level not found'


def test_deleting_security_level(client):
    create_security_level(client)
    response = client.delete(security_level_resource_route, headers=security_level_headers)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message'] == 'Security level deleted'
