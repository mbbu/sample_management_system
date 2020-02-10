from flask_jwt_extended import create_access_token

from api import create_app as app

with app().test_request_context():
    access_token = create_access_token(identity='admin@icipe.org')
    email = 'admin@icipe.org'
    code = '101'

headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'email': email,
    'code': code
}

"""
# ************************************
# ***                              ***
# ***  HELPER FUNCTIONS FOR ROLE   ***
# ***                              ***
# ************************************
"""
role_data = {
    'code': '101',
    'name': 'Admin',
    'description': 'In Charge of the system'
}


def create_role(client):
    response = client.post('/role', json=role_data, headers=headers)
    return response


"""
# ************************************
# ***                              ***
# ***  HELPER FUNCTIONS FOR USER   ***
# ***                              ***
# ************************************
"""
USER_DATA = {
    'first_name': 'ICIPE',
    'last_name': 'ADMIN',
    'email': 'admin@icipe.org',
    'role': '1',
    'password': 'Admin1sMa3str0'
}


def create_user(client):
    response = client.post('/user', json=USER_DATA, headers=headers)
    return response


def prepare_user_test(client):
    create_role(client)
    create_user(client)
