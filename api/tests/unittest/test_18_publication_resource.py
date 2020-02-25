from flask import json

from api.tests.unittest.utils_for_tests import publication_data, create_publication, publication_headers, \
    prepare_publication_test, access_token, publication_updated_data, publication_resource_route, sample_code
from api.utils import format_and_lower_str

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_create_publication_by_non_logged_in_user(client):
    response = client.post(publication_resource_route, json=publication_data)
    assert response.status_code == 401


def test_create_publication(client):
    response = create_publication(client)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['message'] == "Publication successfully created"


def test_create_publication_with_missing_info(client):
    response = client.post(publication_resource_route, json={
        # 'publication_title': publication_code,   <-- missing required info
        'user': 1,
        'sample_results': 'In progress',
        'sample': 1,
        'co_authors': 'Dr Gilbert, Dr Pauline',
    }, headers=publication_headers)

    data = json.loads(response.data)

    assert response.status_code == 400
    assert data['message'] == {
        'publication_title': 'Missing required parameter in the JSON body or the post body or the query '
                             'string'}


def test_create_duplicate_publication(client):
    prepare_publication_test(client)
    response = create_publication(client)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Publication already exists'


"""
# ****************************
# ***                      ***
# ***  TEST GET REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_get_non_existing_publication(client):
    response = client.get(publication_resource_route, headers={'title': 'publication_code'})
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Publication not found'


def test_get_publication(client):
    prepare_publication_test(client)
    response = client.get(publication_resource_route)
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Publications not found'

    elif response.status_code == 200:
        # check that the list is more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; freezer, type and code
        for item in range(len(data['message'])):
            assert data['message'][item]['sample.project'] == 'H3ABNet'
            assert data['message'][item]['sample.code'] == format_and_lower_str(sample_code)
            assert data['message'][item]['user.email'] == 'admin@icipe.org'
            assert data['message'][item]['sample_results'] == 'In progress'
            assert data['message'][item]['publication_title'] == 'rna'
            assert data['message'][item]['co_authors'] == 'Dr Gilbert'
            assert data['message'][item]['sample.theme.name'] == 'Animal Health'


def test_get_publication_by_param(client):
    prepare_publication_test(client)
    response = client.get(publication_resource_route, headers=publication_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message']['sample.project'] == 'H3ABNet'
    assert data['message']['sample.code'] == format_and_lower_str(sample_code)
    assert data['message']['user.email'] == 'admin@icipe.org'
    assert data['message']['sample_results'] == 'In progress'
    assert data['message']['publication_title'] == 'rna'
    assert data['message']['co_authors'] == 'Dr Gilbert'
    assert data['message']['sample.theme.name'] == 'Animal Health'


"""
# ****************************
# ***                      ***
# ***  TEST PUT REQUESTS   ***
# ***                      ***
# ****************************
"""


def test_update_publication_by_non_logged_in_user(client):
    response = client.put(publication_resource_route, json=publication_updated_data)
    assert response.status_code == 401


def test_update_publication(client):
    prepare_publication_test(client)
    response = client.put(publication_resource_route, json=publication_updated_data, headers=publication_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message'] == 'Publication successfully updated'


def test_update_non_existing_publication(client):
    prepare_publication_test(client)
    response = client.put(publication_resource_route, json=publication_updated_data, headers={
        'Authorization': 'Bearer {}'.format(access_token),
        'title': 'publication_code'  # <-- wrong/non-existing code
    })
    data = json.loads(response.data)
    print(data)
    assert response.status_code == 404
    assert data['message'] == 'Publication not found'


def test_update_publication_without_identity(client):
    prepare_publication_test(client)
    response = client.put(publication_resource_route, json=publication_updated_data, headers={
        'Authorization': 'Bearer {}'.format(access_token)  # <-- missing publication code in header
    })
    assert response.status_code == 400


"""
# *****************************
# ***                       ***
# ***  TEST DELETE REQUESTS ***
# ***                       ***
# *****************************
"""


def test_deleting_publication_by_non_logged_in_user(client):
    response = client.delete(publication_resource_route)
    assert response.status_code == 401


def test_deleting_publication_without_identity(client):
    response = client.delete(publication_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token)})
    assert response.status_code == 400


def test_deleting_non_existent_publication(client):
    prepare_publication_test(client)
    response = client.delete(publication_resource_route, headers={'Authorization': 'Bearer {}'.format(access_token),
                                                                  'title': '123'})
    data = json.loads(response.data)
    assert response.status_code == 404
    assert data['message'] == 'Publication not found'


def test_deleting_publication(client):
    prepare_publication_test(client)
    response = client.delete(publication_resource_route, headers=publication_headers)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message'] == 'Publication deleted'
