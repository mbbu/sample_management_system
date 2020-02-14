from flask import json

from api.tests.unittest.utils_for_tests import quantity_type_data, create_quantity_type, quantity_type_headers, \
    access_token, freezer_updated_data, quantity_type_updated_data, quantity_type_code, quantity_type_resource_route

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_quantity_type_by_non_logged_in_user(client):
    response = client.post(quantity_type_resource_route, json=quantity_type_data)
    assert response.status_code == 401


def test_create_quantity_type(client):
    response = create_quantity_type(client)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['message'] == "Quantity type successfully created"


def test_create_quantity_type_with_missing_info(client):
    response = client.post(quantity_type_resource_route, json={
        'code': quantity_type_code,
        # 'name': 'Liters', <-- missing required info
        'description': 'For fluids in large quantities'
    }, headers=quantity_type_headers)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == {'name': 'Missing required parameter in the JSON body or the post body or the query '
                                       'string'}


def test_create_duplicate_quantity_type(client):
    create_quantity_type(client)
    response = create_quantity_type(client)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Quantity type already exists'


"""
# ****************************
# ***                      ***
# ***  TEST GET REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_get_non_existing_quantity_type(client):
    response = client.get(quantity_type_resource_route, headers={'code': 'quantity_type_code'})
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Quantity type not found'


def test_get_quantity_type(client):
    create_quantity_type(client)
    response = client.get(quantity_type_resource_route)
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Quantity types not found'

    elif response.status_code == 200:
        # check that the list is more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; desc, type and code
        for item in range(len(data['message'])):
            assert data['message'][item]['id'] == 'l'
            assert data['message'][item]['name'] == 'Liters'
            assert data['message'][item]['description'] == 'For fluids in large quantities'


def test_get_quantity_type_by_param(client):
    create_quantity_type(client)
    response = client.get(quantity_type_resource_route, headers=quantity_type_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message']['id'] == 'l'
    assert data['message']['name'] == 'Liters'
    assert data['message']['description'] == 'For fluids in large quantities'


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_update_quantity_type_by_non_logged_in_user(client):
    response = client.put(quantity_type_resource_route, json=freezer_updated_data)
    assert response.status_code == 401


def test_update_quantity_type(client):
    create_quantity_type(client)
    response = client.put(quantity_type_resource_route, json=quantity_type_updated_data, headers=quantity_type_headers)
    data = json.loads(response.data)

    assert response.status_code == 202
    assert data['message'] == 'Quantity type successfully updated'


def test_update_non_existing_quantity_type(client):
    create_quantity_type(client)
    response = client.put(quantity_type_resource_route, json=quantity_type_headers, headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'code': 'quantity_type_code'  # <-- wrong/non-existing code
    })
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Quantity type not found'


def test_update_quantity_type_without_identity(client):
    create_quantity_type(client)
    response = client.put(quantity_type_resource_route, json=freezer_updated_data, headers={
        'Authorization': 'Bearer {}'.format(access_token)  # <-- missing quantity_type code in header
    })
    assert response.status_code == 400


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_quantity_type_by_non_logged_in_user(client):
    response = client.delete(quantity_type_resource_route)
    assert response.status_code == 401


def test_deleting_quantity_type_without_identity(client):
    response = client.delete(quantity_type_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token)})
    assert response.status_code == 400


def test_deleting_non_existent_quantity_type(client):
    create_quantity_type(client)
    response = client.delete(quantity_type_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token),
                                                                    'code': '123'})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data['message'] == 'Quantity type not found'

# def test_deleting_quantity_type(client):
#     create_quantity_type(client)
#     response = client.delete(quantity_type_resource_route, headers=quantity_type_headers)
#
#     data = json.loads(response.data)
#     assert response.status_code == 200
#     assert data['message'] == 'Quantity type deleted'
