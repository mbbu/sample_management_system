from flask_jwt_extended import create_access_token

from api import create_app as app

with app().test_request_context():
    access_token = create_access_token(identity='admin@icipe.org')
    email = 'admin@icipe.org'
    role_code = 'Admin1'
    lab_code = 'L1'
    freezer_code = 'L1F1'

headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'email': email,
    'code': role_code
}

"""
# ************************************
# ***                              ***
# ***  HELPER FUNCTIONS FOR ROLE   ***
# ***                              ***
# ************************************
"""
role_data = {
    'code': 'Admin1',
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


"""
# ************************************
# ***                              ***
# ***  HELPER FUNCTIONS FOR LAB   ***
# ***                              ***
# ************************************
"""
lab_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'code': lab_code
}

lab_data = {
    'name': 'R & D',
    'room': '202',
    'code': 'L1'
}


def create_lab(client):
    response = client.post('/lab', json=lab_data, headers=lab_headers)
    return response


"""
# ************************************
# ***                              ***
# ***  HELPER FUNCTIONS FOR FREEZER***
# ***                              ***
# ************************************
"""
freezer_data = {
    'laboratory': '1',
    'room': '303',
    'number': '1',
    'code': 'L1F1'
}

freezer_updated_data = {
    'laboratory': '1',
    'room': '304',  # <-- updated value
    'number': '12',  # <-- updated value
    'code': 'L1F1'
}

freezer_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'code': freezer_code
}


def create_freezer(client):
    response = client.post('/freezer', json=freezer_data, headers=freezer_headers)
    return response


def prepare_freezer_test(client):
    create_lab(client)
    create_freezer(client)
