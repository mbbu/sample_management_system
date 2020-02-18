from flask import json

from api.tests.unittest.utils_for_tests import lab_headers, lab_data, create_lab, access_token, lab_resource_route

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_lab_by_non_logged_in_user(client):
    response = client.post(lab_resource_route, json=lab_data)
    assert response.status_code == 401


def test_create_lab_with_missing_info(client):
    response = client.post(lab_resource_route, json={
        'name': 'R & D',
        # 'room': '202',  <-- required field
        'code': 'ABC'
    }, headers=lab_headers)

    data = json.loads(response.data)
    assert response.status_code == 400
    assert data['message'] == {'room': 'Missing required parameter in the JSON body or the post body or the query '
                                       'string'}


def test_create_lab(client):
    response = create_lab(client)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message'] == 'Successfully Added Laboratory'


def test_create_duplicate_lab(client):
    create_lab(client)
    response = create_lab(client)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Laboratory already exists'


"""
# ****************************
# ***                      ***
# ***  TEST GET REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_get_lab(client):
    create_lab(client)
    response = client.get(lab_resource_route)
    assert b'message' in response.data
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Lab not found'

    elif response.status_code == 200:
        # check that the list is more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; role, email and name(s)
        for item in range(len(data['message'])):
            assert data['message'][item]['name']
            assert data['message'][item]['room']
            assert data['message'][item]['code']


def test_get_user_by_params(client):
    create_lab(client)
    response = client.get(lab_resource_route, headers=lab_headers)
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Lab not found'

    elif response.status_code == 200:
        assert data['message']['name']
        assert data['message']['room']
        assert data['message']['code']


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_update_lab_by_non_logged_in_user(client):
    response = client.put(lab_resource_route, json=lab_data)
    assert response.status_code == 401


def test_update_lab(client):
    create_lab(client)
    response = client.put(lab_resource_route, json={
        'name': 'R & D',
        'room': 'LDH1',
        'code': 'ABC'
    }, headers=lab_headers)

    data = json.loads(response.data)
    assert response.status_code == 202
    assert data['message'] == 'Lab updated successfully'


def test_update_non_existing_lab(client):
    create_lab(client)
    response = client.put(lab_resource_route, json={
        'name': 'R & D',
        'room': '202',
        'code': 'ABC'
    }, headers={'Authorization': 'Bearer {}'.format(access_token),
                'code': 'lab_code'})

    assert response.status_code == 404


def test_update_without_lab_identity(client):
    create_lab(client)
    response = client.put(lab_resource_route, json={
        'name': 'R & D',
        'room': '202',
        'code': 'ABC'
    }, headers={'Authorization': 'Bearer {}'.format(access_token)})

    assert response.status_code == 400


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_lab_without_jwt_token(client):
    response = client.delete(lab_resource_route)
    assert response.status_code == 401


def test_deleting_lab_without_identity(client):
    response = client.delete(lab_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token)})
    assert response.status_code == 400


def test_deleting_non_existent_lab(client):
    create_lab(client)
    response = client.delete(lab_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token),
                                                          'code': '123'})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data['message'] == 'Laboratory does not exist'


def test_deleting_lab(client):
    create_lab(client)
    response = client.delete(lab_resource_route, headers=lab_headers)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message'] == 'Laboratory successfully deleted'
