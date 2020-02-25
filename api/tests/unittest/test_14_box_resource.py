from flask import json

from api.tests.unittest.utils_for_tests import box_data, create_box, box_headers, prepare_box_test, \
    access_token, freezer_updated_data, box_updated_data, box_code, box_resource_route

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_box_by_non_logged_in_user(client):
    response = client.post(box_resource_route, json=box_data)
    assert response.status_code == 401


def test_create_box(client):
    response = create_box(client)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['message'] == "Box successfully created"


def test_create_box_with_missing_info(client):
    response = client.post(box_resource_route, json={
        'tray': '1',
        # 'label': 'animal tissue',    <-- missing required info
        'code': box_code
    }, headers=box_headers)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == {'label': 'Missing required parameter in the JSON body or the post body or the query '
                                        'string'}


def test_create_duplicate_box(client):
    prepare_box_test(client)
    response = create_box(client)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Box already exists'


"""
# ****************************
# ***                      ***
# ***  TEST GET REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_get_non_existing_box(client):
    response = client.get(box_resource_route, headers={'code': 'box_code'})
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Box not found'


def test_get_box(client):
    prepare_box_test(client)
    response = client.get(box_resource_route)
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Boxes not found'

    elif response.status_code == 200:
        # check that the list is more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; freezer, type and code
        for item in range(len(data['message'])):
            assert data['message'][item]['code'] == 'l1f1c1r1t1b1'
            assert data['message'][item]['label'] == 'human skin'
            assert data['message'][item]['tray.number'] == 404
            assert data['message'][item]['tray.rack.number'] == 404
            assert data['message'][item]['tray.rack.chamber.type'] == 'Animal Species'
            assert data['message'][item]['tray.rack.chamber.freezer.number'] == 1
            assert data['message'][item]['tray.rack.chamber.freezer.lab.name'] == 'R & D'
            assert data['message'][item]['tray.rack.chamber.freezer.lab.room'] == 202


def test_get_box_by_param(client):
    prepare_box_test(client)
    response = client.get(box_resource_route, headers=box_headers)
    data = json.loads(response.data)

    assert data['message']['code'] == 'l1f1c1r1t1b1'
    assert data['message']['label'] == 'human skin'
    assert data['message']['tray.number'] == 404
    assert data['message']['tray.rack.number'] == 404
    assert data['message']['tray.rack.chamber.type'] == 'Animal Species'
    assert data['message']['tray.rack.chamber.freezer.number'] == 1
    assert data['message']['tray.rack.chamber.freezer.lab.name'] == 'R & D'
    assert data['message']['tray.rack.chamber.freezer.lab.room'] == 202


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_update_box_by_non_logged_in_user(client):
    response = client.put(box_resource_route, json=freezer_updated_data)
    assert response.status_code == 401


def test_update_box(client):
    prepare_box_test(client)
    response = client.put(box_resource_route, json=box_updated_data, headers=box_headers)
    data = json.loads(response.data)

    assert response.status_code == 202
    assert data['message'] == 'Box successfully updated'


def test_update_non_existing_box(client):
    prepare_box_test(client)
    response = client.put(box_resource_route, json=box_headers, headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'code': 'box_code'  # <-- wrong/non-existing code
    })
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Box not found'


def test_update_box_without_identity(client):
    prepare_box_test(client)
    response = client.put(box_resource_route, json=freezer_updated_data, headers={
        'Authorization': 'Bearer {}'.format(access_token)  # <-- missing box code in header
    })
    assert response.status_code == 400


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_box_by_non_logged_in_user(client):
    response = client.delete(box_resource_route)
    assert response.status_code == 401


def test_deleting_box_without_identity(client):
    response = client.delete(box_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token)})
    assert response.status_code == 400


def test_deleting_non_existent_box(client):
    prepare_box_test(client)
    response = client.delete(box_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token),
                                                          'code': '123'})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data['message'] == 'Box not found'


def test_deleting_box(client):
    prepare_box_test(client)
    response = client.delete(box_resource_route, headers=box_headers)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message'] == 'Box deleted'
