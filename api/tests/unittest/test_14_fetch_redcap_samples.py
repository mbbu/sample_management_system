from flask import json

from api.tests.unittest.utils_for_tests import redcap_sample_resource_route, create_sample_from_redcap, \
    redcap_sample_headers, redcap_sample_data

"""
# ****************************
# ***                      ***
# ***  TEST POST REQUESTS  ***
# ***                      ***
# ****************************
"""


def test_fetch_samples_from_redcap_by_non_logged_in_user(client):
    response = client.post(redcap_sample_resource_route)
    assert response.status_code == 401


def test_fetch_and_save_samples_from_redcap(client):
    response = create_sample_from_redcap(client)
    data = json.loads(response.data)

    assert response.status_code == 201
    assert data['message'] == "Samples successfully fetched and saved"


def test_fetch_and_save_samples_from_redcap_with_filters(client):
    response = client.post(redcap_sample_resource_route, json=redcap_sample_data, headers=redcap_sample_headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message'] == "Samples from date {0} to date {1} saved".format(redcap_sample_data['start_date'],
                                                                               redcap_sample_data['end_date'])


def test_fetch_and_save_samples_when_redcap_is_unavailable(client):
    response = create_sample_from_redcap(client)
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'Redcap error. Admin contacted.'


def test_fetch_and_save_duplicate_samples(client):
    create_sample_from_redcap(client)
    response = create_sample_from_redcap(client)
    data = json.loads(response.data)

    assert response.status_code == 409
    assert data['message'] == 'Sample already exists'
