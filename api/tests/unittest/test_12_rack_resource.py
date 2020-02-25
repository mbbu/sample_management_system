from flask import json

from api.tests.unittest.utils_for_tests import rack_data, create_rack, rack_headers, prepare_rack_test, \
    access_token, freezer_updated_data, rack_updated_data, rack_resource_route

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_rack_by_non_logged_in_user(client):
    response = client.post(rack_resource_route, json=rack_data)
    assert response.status_code == 401


def test_create_rack(client):
    response = create_rack(client)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['message'] == "Rack successfully created"


def test_create_rack_with_missing_info(client):
    response = client.post(rack_resource_route, json={
        'chamber': '1',
        # 'number': '405',    <-- missing required info
        'code': 'L1F1C1R1'
    }, headers=rack_headers)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == {'number': 'Missing required parameter in the JSON body or the post body or the query '
                                         'string'}


def test_create_duplicate_rack(client):
    prepare_rack_test(client)
    response = create_rack(client)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Rack already exists'


"""
# ****************************
# ***                      ***
# ***  TEST GET REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_get_non_existing_rack(client):
    response = client.get(rack_resource_route, headers={'code': 'rack_code'})
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Rack not found'


def test_get_rack(client):
    prepare_rack_test(client)
    response = client.get(rack_resource_route)
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Racks not found'

    elif response.status_code == 200:
        # check that the list is more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; freezer, type and code
        for item in range(len(data['message'])):
            assert data['message'][item]['number'] == 404
            assert data['message'][item]['chamber.type'] == 'Animal Species'
            assert data['message'][item]['code'] == 'l1f1c1r1'


def test_get_rack_by_param(client):
    prepare_rack_test(client)
    response = client.get(rack_resource_route, headers=rack_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message']['number'] == 404
    assert data['message']['chamber.type'] == 'Animal Species'
    assert data['message']['code'] == 'l1f1c1r1'


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_update_rack_by_non_logged_in_user(client):
    response = client.put(rack_resource_route, json=freezer_updated_data)
    assert response.status_code == 401


def test_update_rack(client):
    prepare_rack_test(client)
    response = client.put(rack_resource_route, json=rack_updated_data, headers=rack_headers)
    data = json.loads(response.data)

    assert response.status_code == 202
    assert data['message'] == 'Rack successfully updated'


def test_update_non_existing_rack(client):
    prepare_rack_test(client)
    response = client.put(rack_resource_route, json=rack_headers, headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'code': 'rack_code'  # <-- wrong/non-existing code
    })
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Rack not found'


def test_update_rack_without_identity(client):
    prepare_rack_test(client)
    response = client.put(rack_resource_route, json=freezer_updated_data, headers={
        'Authorization': 'Bearer {}'.format(access_token)  # <-- missing rack code in header
    })
    assert response.status_code == 400


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_rack_by_non_logged_in_user(client):
    response = client.delete(rack_resource_route)
    assert response.status_code == 401


def test_deleting_rack_without_identity(client):
    response = client.delete(rack_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token)})
    assert response.status_code == 400


def test_deleting_non_existent_rack(client):
    prepare_rack_test(client)
    response = client.delete(rack_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token),
                                                           'code': '123'})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data['message'] == 'Rack not found'


def test_deleting_rack(client):
    prepare_rack_test(client)
    response = client.delete(rack_resource_route, headers=rack_headers)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message'] == 'Rack deleted'
