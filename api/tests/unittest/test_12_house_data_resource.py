from flask import json

from api.tests.unittest.utils_for_tests import house_data_data, create_house_data, house_data_headers, \
    house_data_updated_data, access_token

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_house_data_by_non_logged_in_user(client):
    response = client.post('/house-data', json=house_data_data)
    assert response.status_code == 401


def test_create_house_data(client):
    response = create_house_data(client)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['message'] == "House data successfully created"


def test_create_house_data_with_missing_info(client):
    response = client.post('/house-data', json={
        # 'code': house_data_code, <-- missing required param
        'user': 1,
        'education': 'Tertiary',
        'employment': 'Formal',
        'marital_status': 'Married',
        'people': '3',
        'children': '1',
        'animals': '5',
        'economic_activity': 'farming',
        'type_of_animals': 'cattle',
        'farming_activities': 'cattle farming',
        'social_economic_data': 'None'
    }, headers=house_data_headers)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == {'code': 'Missing required parameter in the JSON body or the post body or the query '
                                       'string'}


def test_create_duplicate_house_data(client):
    create_house_data(client)
    response = create_house_data(client)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'House data already exists'


"""
# ****************************
# ***                      ***
# ***  TEST GET REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_get_non_existing_house_data(client):
    response = client.get('/house-data', headers={'code': 'house_data_code'})
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'House data not found'


def test_get_house_data(client):
    create_house_data(client)
    response = client.get('/house-data')
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'House data not found'

    elif response.status_code == 200:
        # check that the list is more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; code, name ...
        for item in range(len(data['message'])):
            assert data['message'][item]['code'] == 'h1'
            assert data['message'][item]['user_id'] == 1
            assert data['message'][item]['education'] == 'Tertiary'
            assert data['message'][item]['employment'] == 'Formal'
            assert data['message'][item]['marital_status'] == 'Married'
            assert data['message'][item]['number_of_people'] == 3
            assert data['message'][item]['number_of_children'] == 1
            assert data['message'][item]['number_of_animals'] == 5
            assert data['message'][item]['economic_activity'] == 'farming'
            assert data['message'][item]['type_of_animals'] == 'cattle'
            assert data['message'][item]['farming_activities'] == 'cattle farming'
            assert data['message'][item]['social_economic_data'] == True


def test_get_house_data_by_param(client):
    create_house_data(client)
    response = client.get('/house-data', headers=house_data_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message']['code'] == 'h1'
    assert data['message']['user_id'] == 1
    assert data['message']['education'] == 'Tertiary'
    assert data['message']['employment'] == 'Formal'
    assert data['message']['marital_status'] == 'Married'
    assert data['message']['number_of_people'] == 3
    assert data['message']['number_of_children'] == 1
    assert data['message']['number_of_animals'] == 5
    assert data['message']['economic_activity'] == 'farming'
    assert data['message']['type_of_animals'] == 'cattle'
    assert data['message']['farming_activities'] == 'cattle farming'
    assert data['message']['social_economic_data'] == True


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_update_house_data_by_non_logged_in_user(client):
    response = client.put('/house-data', json=house_data_updated_data)
    assert response.status_code == 401


def test_update_house_data(client):
    create_house_data(client)
    response = client.put('/house-data', json=house_data_updated_data, headers=house_data_headers)
    data = json.loads(response.data)

    assert response.status_code == 202
    assert data['message'] == 'House data successfully updated'


def test_update_non_existing_house_data(client):
    create_house_data(client)
    response = client.put('/house-data', json=house_data_headers, headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'code': 'house_data_code'  # <-- wrong/non-existing code
    })
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'House data not found'


def test_update_house_data_without_identity(client):
    create_house_data(client)
    response = client.put('/house-data', json=house_data_updated_data, headers={
        'Authorization': 'Bearer {}'.format(access_token)  # <-- missing house_data code in header
    })
    assert response.status_code == 400


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_house_data_by_non_logged_in_user(client):
    response = client.delete('/house-data')
    assert response.status_code == 401


def test_deleting_house_data_without_identity(client):
    response = client.delete('/house-data', headers={'Authorization': 'Bearer {}'.format(access_token)})
    assert response.status_code == 400


def test_deleting_non_existent_house_data(client):
    create_house_data(client)
    response = client.delete('/house-data', headers={'Authorization': 'Bearer {}'.format(access_token),
                                                     'code': '123'})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data['message'] == 'House data not found'


def test_deleting_house_data(client):
    create_house_data(client)
    response = client.delete('/house-data', headers=house_data_headers)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message'] == 'House data deleted'
