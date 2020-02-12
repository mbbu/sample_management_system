from flask import json

from api.tests.unittest.utils_for_tests import freezer_data, create_freezer, freezer_headers, prepare_freezer_test, \
    access_token, freezer_updated_data

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_freezer_by_non_logged_in_user(client):
    response = client.post('/freezer', json=freezer_data)
    assert response.status_code == 401


def test_create_freezer(client):
    response = create_freezer(client)
    data = json.loads(response.data)

    print(data)
    assert response.status_code == 201
    assert data['message'] == "Freezer Successfully Created"


def test_create_freezer_with_missing_info(client):
    response = client.post('/freezer', json={
        'laboratory': '1',
        'number': '1',
        # 'room': '303', <-- missing required field
        'code': 'L1F1'
    }, headers=freezer_headers)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == {'room': 'Missing required parameter in the JSON body or the post body or the query '
                                       'string'}


def test_create_duplicate_freezer(client):
    prepare_freezer_test(client)
    response = create_freezer(client)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Freezer already exists'


"""
# ****************************
# ***                      ***
# ***  TEST GET REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_non_existing_freezer(client):
    response = client.get('/freezer', headers={'code': 'freezer_code'})
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Freezer not found'


def test_get_freezer(client):
    prepare_freezer_test(client)
    response = client.get('/freezer')
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Freezers not found'

    elif response.status_code == 200:
        # check that the list is more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; freezer, type and code
        for item in range(len(data['message'])):
            assert data['message'][item]['lab.name'] == 'R & D'
            assert data['message'][item]['room'] == '303'
            assert data['message'][item]['number'] == 1
            assert data['message'][item]['code'] == 'l1f1'


def test_get_freezer_by_param(client):
    prepare_freezer_test(client)
    response = client.get('/freezer', headers=freezer_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message']['lab.name'] == 'R & D'
    assert data['message']['room'] == '303'
    assert data['message']['number'] == 1
    assert data['message']['code'] == 'l1f1'


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_update_freezer_by_non_logged_in_user(client):
    response = client.put('/freezer', json=freezer_updated_data)
    assert response.status_code == 401


def test_update_freezer(client):
    prepare_freezer_test(client)
    response = client.put('/freezer', json=freezer_updated_data, headers=freezer_headers)
    data = json.loads(response.data)

    assert response.status_code == 202
    assert data['message'] == 'Successfully updated freezer'


def test_update_non_existing_freezer(client):
    prepare_freezer_test(client)
    response = client.put('/freezer', json=freezer_headers, headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'code': 'freezer_code'  # <-- wrong/non-existing code
    })
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Freezer does not exist'


def test_update_freezer_without_identity(client):
    prepare_freezer_test(client)
    response = client.put('/freezer', json=freezer_updated_data, headers={
        'Authorization': 'Bearer {}'.format(access_token)  # <-- missing freezer code in header
    })
    assert response.status_code == 400


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_freezer_by_non_logged_in_user(client):
    response = client.delete('/freezer')
    assert response.status_code == 401


def test_deleting_freezer_without_identity(client):
    response = client.delete('/freezer', headers={'Authorization': 'Bearer {}'.format(access_token)})
    assert response.status_code == 400


def test_deleting_non_existent_freezer(client):
    prepare_freezer_test(client)
    response = client.delete('/freezer', headers={'Authorization': 'Bearer {}'.format(access_token),
                                                  'code': '123'})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data['message'] == 'Freezer does not exist'


def test_deleting_freezer(client):
    prepare_freezer_test(client)
    response = client.delete('/freezer', headers=freezer_headers)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message'] == 'Freezer deleted'
