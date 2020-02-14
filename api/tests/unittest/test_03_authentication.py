from flask import json

from api.tests.unittest.utils_for_tests import prepare_user_test, headers

login_details = {
    'email': 'admin@icipe.org',
    'password': 'Admin1sMa3str0'
}

wrong_login_details = {
    'email': 'admin@icipe.org',
    'password': 'Admin1sMa3str0!!'
}

non_existent_user = {
    'email': 'admins@icipe.org',
    'password': 'Admin1sMa3str0!!'
}

"""
# ****************************
# ***                      ***
# ***  TEST LOGOUT         ***
# ***                      ***
# ****************************
"""


def test_login(client):
    prepare_user_test(client)
    response = client.post('/auth', json=login_details)

    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message']['first_name'] and data['message']['first_name'] == 'ICIPE'
    assert data['message']['last_name'] and data['message']['last_name'] == 'ADMIN'
    assert data['message']['email'] and data['message']['email'] == 'admin@icipe.org'
    assert data['message']['token']
    assert data['message']['refresh_token']


def test_login_wrong_credentials(client):
    prepare_user_test(client)
    response = client.post('/auth', json=wrong_login_details)
    data = json.loads(response.data)

    assert response.status_code == 403
    assert data['message'] == 'Wrong password try again'


def test_non_existent_user(client):
    prepare_user_test(client)
    response = client.post('/auth', json=non_existent_user)
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['message'] == 'User not found'


# todo: test the token generated is a jwt token


"""
# ****************************
# ***                      ***
# ***  TEST LOGOUT         ***
# ***                      ***
# ****************************
"""


def test_logout(client):
    prepare_user_test(client)
    response = client.get('/logout', headers=headers)
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['message'] == 'Successfully Logged Out'


def test_logout_non_logged_in_user(client):
    prepare_user_test(client)
    response = client.get('/logout')

    assert response.status_code == 401
