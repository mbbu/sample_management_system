from flask import json

from api.tests.unittest.utils_for_tests import chamber_data, create_chamber, chamber_headers, prepare_chamber_test, \
    access_token, freezer_updated_data, chamber_updated_data

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_chamber_by_non_logged_in_user(client):
    response = client.post('/chamber', json=chamber_data)
    assert response.status_code == 401


def test_create_chamber(client):
    response = create_chamber(client)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['message'] == "Chamber successfully created"


def test_create_chamber_with_missing_info(client):
    response = client.post('/chamber', json={
        'freezer': '1',
        # 'type': 'Animal Species',  <-- missing required info
        'code': 'L1F1C1'
    }, headers=chamber_headers)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == {'type': 'Missing required parameter in the JSON body or the post body or the query '
                                       'string'}


def test_create_duplicate_chamber(client):
    prepare_chamber_test(client)
    response = create_chamber(client)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Chamber already exists'


"""
# ****************************
# ***                      ***
# ***  TEST GET REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_get_non_existing_chamber(client):
    response = client.get('/chamber', headers={'code': 'chamber_code'})
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Chamber not found'


def test_get_chamber(client):
    prepare_chamber_test(client)
    response = client.get('/chamber')
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Chambers not found'

    elif response.status_code == 200:
        # check that the list is more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; freezer, type and code
        for item in range(len(data['message'])):
            assert data['message'][item]['freezer.number'] == '1'
            assert data['message'][item]['freezer.room'] == '303'
            assert data['message'][item]['type'] == 'Animal Species'
            assert data['message'][item]['code'] == 'l1f1c1'


def test_get_chamber_by_param(client):
    prepare_chamber_test(client)
    response = client.get('/chamber', headers=chamber_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message']['freezer.number'] == '1'
    assert data['message']['freezer.room'] == '303'
    assert data['message']['type'] == 'Animal Species'
    assert data['message']['code'] == 'l1f1c1'


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_update_chamber_by_non_logged_in_user(client):
    response = client.put('/chamber', json=freezer_updated_data)
    assert response.status_code == 401


def test_update_chamber(client):
    prepare_chamber_test(client)
    response = client.put('/chamber', json=chamber_updated_data, headers=chamber_headers)
    data = json.loads(response.data)

    assert response.status_code == 202
    assert data['message'] == 'Chamber successfully updated'


def test_update_non_existing_chamber(client):
    prepare_chamber_test(client)
    response = client.put('/chamber', json=chamber_headers, headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'code': 'chamber_code'  # <-- wrong/non-existing code
    })
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Chamber not found'


def test_update_chamber_without_identity(client):
    prepare_chamber_test(client)
    response = client.put('/chamber', json=freezer_updated_data, headers={
        'Authorization': 'Bearer {}'.format(access_token)  # <-- missing chamber code in header
    })
    assert response.status_code == 400


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_chamber_by_non_logged_in_user(client):
    response = client.delete('/chamber')
    assert response.status_code == 401


def test_deleting_chamber_without_identity(client):
    response = client.delete('/chamber', headers={'Authorization': 'Bearer {}'.format(access_token)})
    assert response.status_code == 400


def test_deleting_non_existent_chamber(client):
    prepare_chamber_test(client)
    response = client.delete('/chamber', headers={'Authorization': 'Bearer {}'.format(access_token),
                                                  'code': '123'})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data['message'] == 'Chamber not found'

# def test_deleting_chamber(client):
#     prepare_chamber_test(client)
#     response = client.delete('/chamber', headers=chamber_headers)
#
#     data = json.loads(response.data)
#     assert response.status_code == 200
#     assert data['message'] == 'Chamber deleted'
