from flask import json

from api.tests.unittest.utils_for_tests import theme_data, create_theme, theme_code, theme_headers, theme_updated_data, \
    access_token, theme_resource_route

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_theme_by_non_logged_in_user(client):
    response = client.post(theme_resource_route, json=theme_data)
    data = json.loads(response.data)
    assert response.status_code == 401
    assert data['msg'] == 'Missing Authorization Header'


def test_create_theme(client):
    response = create_theme(client)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['message'] == "Theme successfully created"


def test_create_theme_with_missing_info(client):
    response = client.post(theme_resource_route, json={
        # 'name': 'Animal Health', <-- missing required info
        'code': theme_code
    }, headers=theme_headers)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == {'name': 'Missing required parameter in the JSON body or the post body or the query '
                                       'string'}


def test_create_duplicate_theme(client):
    create_theme(client)
    response = create_theme(client)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Theme already exists'


"""
# ****************************
# ***                      ***
# ***  TEST GET REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_get_non_existing_theme(client):
    response = client.get(theme_resource_route, headers={'code': 'theme_code'})
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Theme not found'


def test_get_theme(client):
    create_theme(client)
    response = client.get(theme_resource_route)
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Themes not found'

    elif response.status_code == 200:
        # check that the list is more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; name and code
        for item in range(len(data['message'])):
            assert data['message'][item]['code'] == 'ah'
            assert data['message'][item]['name'] == 'Animal Health'


def test_get_theme_by_param(client):
    create_theme(client)
    response = client.get(theme_resource_route, headers=theme_headers)
    data = json.loads(response.data)

    assert data['message']['code'] == 'ah'
    assert data['message']['name'] == 'Animal Health'


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_update_theme_by_non_logged_in_user(client):
    response = client.put(theme_resource_route, json=theme_updated_data)
    data = json.loads(response.data)
    assert response.status_code == 401
    assert data['msg'] == 'Missing Authorization Header'


def test_update_theme(client):
    create_theme(client)
    response = client.put(theme_resource_route, json=theme_updated_data, headers=theme_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message'] == 'Theme successfully updated'


def test_update_non_existing_theme(client):
    create_theme(client)
    response = client.put(theme_resource_route, json=theme_updated_data, headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'code': 'theme_code'  # <-- wrong/non-existing code
    })
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Theme not found'


def test_update_theme_without_identity(client):
    create_theme(client)
    response = client.put(theme_resource_route, json=theme_updated_data, headers={
        'Authorization': 'Bearer {}'.format(access_token)  # <-- missing theme code in header
    })
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'Expected an identifier i.e code or label to perform action. ' \
                              'Pass the same in request header'


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_theme_by_non_logged_in_user(client):
    response = client.delete(theme_resource_route)
    data = json.loads(response.data)
    assert response.status_code == 401
    assert data['msg'] == 'Missing Authorization Header'


def test_deleting_theme_without_identity(client):
    response = client.delete(theme_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token)})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == 'Expected an identifier i.e code or label to perform action. ' \
                              'Pass the same in request header'


def test_deleting_non_existent_theme(client):
    create_theme(client)
    response = client.delete(theme_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token),
                                                            'code': '123'})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data['message'] == 'Theme not found'


def test_deleting_theme(client):
    create_theme(client)
    response = client.delete(theme_resource_route, headers=theme_headers)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message'] == 'Theme deleted'
