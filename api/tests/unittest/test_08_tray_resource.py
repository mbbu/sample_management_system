from flask import json

from api.tests.unittest.utils_for_tests import tray_data, create_tray, tray_headers, prepare_tray_test, \
    access_token, freezer_updated_data, tray_updated_data, tray_code

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_tray_by_non_logged_in_user(client):
    response = client.post('/tray', json=tray_data)
    assert response.status_code == 401


def test_create_tray(client):
    response = create_tray(client)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['message'] == "Tray successfully created"


def test_create_tray_with_missing_info(client):
    response = client.post('/tray', json={
        'rack': '1',
        # 'number': '405',    <-- missing required info
        'code': tray_code
    }, headers=tray_headers)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == {'number': 'Missing required parameter in the JSON body or the post body or the query '
                                         'string'}


def test_create_duplicate_tray(client):
    prepare_tray_test(client)
    response = create_tray(client)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Tray already exists'


"""
# ****************************
# ***                      ***
# ***  TEST GET REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_get_non_existing_tray(client):
    response = client.get('/tray', headers={'code': 'tray_code'})
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Tray not found'


def test_get_tray(client):
    prepare_tray_test(client)
    response = client.get('/tray')
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Trays not found'

    elif response.status_code == 200:
        # check that the list is more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; freezer, type and code
        for item in range(len(data['message'])):
            assert data['message'][item]['number'] == 404
            assert data['message'][item]['rack.number'] == 404
            assert data['message'][item]['code'] == 'l1f1c1r1t1'


def test_get_tray_by_param(client):
    prepare_tray_test(client)
    response = client.get('/tray', headers=tray_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message']['number'] == 404
    assert data['message']['rack.number'] == 404
    assert data['message']['code'] == 'l1f1c1r1t1'


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_update_tray_by_non_logged_in_user(client):
    response = client.put('/tray', json=freezer_updated_data)
    assert response.status_code == 401


def test_update_tray(client):
    prepare_tray_test(client)
    response = client.put('/tray', json=tray_updated_data, headers=tray_headers)
    data = json.loads(response.data)

    assert response.status_code == 202
    assert data['message'] == 'Tray successfully updated'


def test_update_non_existing_tray(client):
    prepare_tray_test(client)
    response = client.put('/tray', json=tray_headers, headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'code': 'tray_code'  # <-- wrong/non-existing code
    })
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Tray not found'


def test_update_tray_without_identity(client):
    prepare_tray_test(client)
    response = client.put('/tray', json=freezer_updated_data, headers={
        'Authorization': 'Bearer {}'.format(access_token)  # <-- missing tray code in header
    })
    assert response.status_code == 400


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_tray_by_non_logged_in_user(client):
    response = client.delete('/tray')
    assert response.status_code == 401


def test_deleting_tray_without_identity(client):
    response = client.delete('/tray', headers={'Authorization': 'Bearer {}'.format(access_token)})
    assert response.status_code == 400


def test_deleting_non_existent_tray(client):
    prepare_tray_test(client)
    response = client.delete('/tray', headers={'Authorization': 'Bearer {}'.format(access_token),
                                               'code': '123'})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data['message'] == 'Tray not found'


def test_deleting_tray(client):
    prepare_tray_test(client)
    response = client.delete('/tray', headers=tray_headers)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message'] == 'Tray deleted'
