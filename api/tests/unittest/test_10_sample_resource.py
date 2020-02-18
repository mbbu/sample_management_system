from flask import json

from api.tests.unittest.utils_for_tests import sample_data, create_sample, sample_headers, prepare_sample_test, \
    access_token, sample_updated_data, sample_code, sample_resource_route
from api.utils import format_and_lower_str

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_sample_by_non_logged_in_user(client):
    response = client.post(sample_resource_route, json=sample_data)
    assert response.status_code == 401


def test_create_sample(client):
    response = create_sample(client)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['message'] == "Sample successfully created"


def test_create_sample_with_missing_info(client):
    response = client.post(sample_resource_route, json={
        # 'theme_id': 1, <-- missing required info
        'user_id': 1,
        'box_id': 1,
        'animal_species': 'Insects',
        'sample_type': 'Mosquito',
        'sample_description': 'Kwale mosquito samples',
        'location_collected': 'Kwale',
        'project': 'H3ABNet',
        'project_owner': 'Dr Careen',
        'retention_period': 3,
        'barcode': '12254DS5774SDFS',
        'analysis': 'Incomplete',
        'temperature': 35.0,
        'amount': 100,
        'quantity_type': 'l',
        'security_level': 1,
        'code': sample_code
    }, headers=sample_headers)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == {'theme': 'Missing required parameter in the JSON body or the post body or the query '
                                        'string'}


def test_create_duplicate_sample(client):
    prepare_sample_test(client)
    response = create_sample(client)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Sample already exists'


"""
# ****************************
# ***                      ***
# ***  TEST GET REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_get_non_existing_sample(client):
    response = client.get(sample_resource_route, headers={'code': 'sample_code'})
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Sample not found'


def test_get_sample(client):
    prepare_sample_test(client)
    response = client.get(sample_resource_route)
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Samples not found'

    elif response.status_code == 200:
        # check that the list is more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; freezer, type and code
        for item in range(len(data['message'])):
            assert data['message'][item]['theme.name'] == 'Animal Health'
            assert data['message'][item]['user.email'] == 'admin@icipe.org'
            assert data['message'][item]['box.label'] == 'human skin'
            assert data['message'][item]['animal_species'] == 'Insects'
            assert data['message'][item]['sample_type'] == 'Mosquito'
            assert data['message'][item]['sample_description'] == 'Kwale mosquito samples'
            assert data['message'][item]['location_collected'] == 'Kwale'
            assert data['message'][item]['project'] == 'H3ABNet'
            assert data['message'][item]['project_owner'] == 'Dr Careen'
            assert data['message'][item]['retention_period'] == 3
            assert data['message'][item]['barcode'] == '12254DS5774SDFS'
            assert data['message'][item]['analysis'] == 'Incomplete'
            assert data['message'][item]['temperature'] == '35.00'
            assert data['message'][item]['amount'] == 100
            assert data['message'][item]['quantity.id'] == 'l'
            assert data['message'][item]['security_level'] == 1
            assert data['message'][item]['code'] == format_and_lower_str(sample_code)()


def test_get_sample_by_param(client):
    prepare_sample_test(client)
    response = client.get(sample_resource_route, headers=sample_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message']['theme.name'] == 'Animal Health'
    assert data['message']['user.email'] == 'admin@icipe.org'
    assert data['message']['box.label'] == 'human skin'
    assert data['message']['animal_species'] == 'Insects'
    assert data['message']['sample_type'] == 'Mosquito'
    assert data['message']['sample_description'] == 'Kwale mosquito samples'
    assert data['message']['location_collected'] == 'Kwale'
    assert data['message']['project'] == 'H3ABNet'
    assert data['message']['project_owner'] == 'Dr Careen'
    assert data['message']['retention_period'] == 3
    assert data['message']['barcode'] == '12254DS5774SDFS'
    assert data['message']['analysis'] == 'Incomplete'
    assert data['message']['temperature'] == '35.00'
    assert data['message']['amount'] == 100
    assert data['message']['quantity.id'] == 'l'
    assert data['message']['security_level'] == 1
    assert data['message']['code'] == format_and_lower_str(sample_code)()


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_update_sample_by_non_logged_in_user(client):
    response = client.put(sample_resource_route, json=sample_updated_data)
    assert response.status_code == 401


def test_update_sample(client):
    prepare_sample_test(client)
    response = client.put(sample_resource_route, json=sample_updated_data, headers=sample_headers)
    data = json.loads(response.data)

    assert response.status_code == 202
    assert data['message'] == 'Sample successfully updated'


def test_update_non_existing_sample(client):
    prepare_sample_test(client)
    response = client.put(sample_resource_route, json=sample_headers, headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'code': 'sample_code'  # <-- wrong/non-existing code
    })
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Sample not found'


def test_update_sample_without_identity(client):
    prepare_sample_test(client)
    response = client.put(sample_resource_route, json=sample_updated_data, headers={
        'Authorization': 'Bearer {}'.format(access_token)  # <-- missing sample code in header
    })
    assert response.status_code == 400


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_sample_by_non_logged_in_user(client):
    response = client.delete(sample_resource_route)
    assert response.status_code == 401


def test_deleting_sample_without_identity(client):
    response = client.delete(sample_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token)})
    assert response.status_code == 400


def test_deleting_non_existent_sample(client):
    prepare_sample_test(client)
    response = client.delete(sample_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token),
                                                             'code': '123'})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data['message'] == 'Sample not found'


def test_deleting_sample(client):
    prepare_sample_test(client)
    response = client.delete(sample_resource_route, headers=sample_headers)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message'] == 'Sample deleted'
