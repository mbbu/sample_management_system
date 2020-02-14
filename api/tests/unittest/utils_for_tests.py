from flask_jwt_extended import create_access_token

from api import create_app as app

with app().test_request_context():
    access_token = create_access_token(identity='admin@icipe.org')
    email = 'admin@icipe.org'
    theme_code = "AH"
    role_code = 'Admin1'
    lab_code = 'L1'
    freezer_code = 'L1F1'
    chamber_code = 'L1F1C1'
    rack_code = 'L1F1C1R1'
    tray_code = 'L1F1C1R1T1'
    box_code = 'L1F1C1R1T1B1'
    security_level_code = 'A1'
    house_data_code = 'H1'
    quantity_type_code = 'L'
    sample_code = 'S1'
    publication_code = 'rNA'

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
    'code': freezer_code
}

freezer_updated_data = {
    'laboratory': '1',
    'room': '304',  # <-- updated value
    'number': '12',  # <-- updated value
    'code': freezer_code
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


"""
# ************************************
# ***                              ***
# ***  HELPER FUNCTIONS FOR CHAMBER***
# ***                              ***
# ************************************
"""
chamber_data = {
    'freezer': '1',
    'type': 'Animal Species',
    'code': chamber_code
}

chamber_updated_data = {
    'freezer': '1',
    'type': 'Plant Species',  # <-- updated value
    'code': chamber_code
}

chamber_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'code': chamber_code
}


def create_chamber(client):
    response = client.post('/chamber', json=chamber_data, headers=chamber_headers)
    return response


def prepare_chamber_test(client):
    create_lab(client)
    create_freezer(client)
    create_chamber(client)


"""
# ************************************
# ***                              ***
# ***  HELPER FUNCTIONS FOR RACK   ***
# ***                              ***
# ************************************
"""
rack_data = {
    'chamber': '1',
    'number': '404',
    'code': rack_code
}

rack_updated_data = {
    'chamber': '1',
    'number': '405',  # <-- updated value
    'code': rack_code
}

rack_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'code': rack_code
}


def create_rack(client):
    response = client.post('/rack', json=rack_data, headers=rack_headers)
    return response


def prepare_rack_test(client):
    create_lab(client)
    create_freezer(client)
    create_chamber(client)
    create_rack(client)


"""
# ************************************
# ***                              ***
# ***  HELPER FUNCTIONS FOR TRAY   ***
# ***                              ***
# ************************************
"""
tray_data = {
    'rack': '1',
    'number': '404',
    'code': tray_code
}

tray_updated_data = {
    'rack': '1',
    'number': '405',  # <-- updated value
    'code': tray_code
}

tray_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'code': tray_code
}


def create_tray(client):
    response = client.post('/tray', json=tray_data, headers=tray_headers)
    return response


def prepare_tray_test(client):
    create_lab(client)
    create_freezer(client)
    create_chamber(client)
    create_rack(client)
    create_tray(client)


"""
# ************************************
# ***                              ***
# ***  HELPER FUNCTIONS FOR BOX    ***
# ***                              ***
# ************************************
"""
box_data = {
    'tray': '1',
    'label': 'human skin',
    'code': box_code
}

box_updated_data = {
    'tray': '1',
    'label': 'animal tissue',  # <-- updated value
    'code': box_code
}

box_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'code': box_code
}


def create_box(client):
    response = client.post('/box', json=box_data, headers=box_headers)
    return response


def prepare_box_test(client):
    create_lab(client)
    create_freezer(client)
    create_chamber(client)
    create_rack(client)
    create_tray(client)
    create_box(client)


"""
# ************************************
# ***                              ***
# ***  HELPER FUNCTIONS FOR THEME  ***
# ***                              ***
# ************************************
"""
theme_data = {
    'name': 'Animal Health',
    'code': theme_code
}

theme_updated_data = {
    'name': 'Human Health',  # <-- updated value
    'code': theme_code
}

theme_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'code': theme_code
}


def create_theme(client):
    response = client.post('/theme', json=theme_data, headers=theme_headers)
    return response


"""
# *********************************************
# ***                                       ***
# ***  HELPER FUNCTIONS FOR SECURITY LEVEL  ***
# ***                                       ***
# *********************************************
"""
security_level_data = {
    'name': 'Ebola',
    'code': security_level_code,
    'description': 'CDC L1'
}

security_level_updated_data = {
    'name': 'Corona Virus',  # <-- updated value
    'code': security_level_code,
    'description': 'CDC L1'
}

security_level_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'code': security_level_code
}


def create_security_level(client):
    response = client.post('/security-level', json=security_level_data, headers=security_level_headers)
    return response


"""
# *********************************************
# ***                                       ***
# ***  HELPER FUNCTIONS FOR QUANTITY TYPE   ***
# ***                                       ***
# *********************************************
"""
quantity_type_resource_route = '/quantity-type'
quantity_type_data = {
    'code': quantity_type_code,
    'name': 'Liters',
    'description': 'For fluids in large quantities'
}

quantity_type_updated_data = {
    'code': quantity_type_code,
    'name': 'Litres',  # <-- updated value
    'description': 'For fluids in large quantities'
}

quantity_type_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'code': quantity_type_code
}


def create_quantity_type(client):
    response = client.post(quantity_type_resource_route, json=quantity_type_data, headers=quantity_type_headers)
    return response


"""
# *********************************************
# ***                                       ***
# ***  HELPER FUNCTIONS FOR SAMPLE          ***
# ***                                       ***
# *********************************************
"""
sample_resource_route = '/sample'
sample_data = {
    'theme': 1,
    'user': 1,
    'box': 1,
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
}

sample_updated_data = {
    'theme': 1,
    'user': 1,
    'box': 1,
    'animal_species': 'Insects',
    'sample_type': 'Mosquito',
    'sample_description': 'Kwale mosquito samples',
    'location_collected': 'Kwale',
    'project': 'H3ABNet',
    'project_owner': 'Dr Careen',
    'retention_period': 3,
    'barcode': '12254DS5774SDFS',
    'analysis': 'Complete',  # <-- updated value
    'temperature': 35.0,
    'amount': 100,
    'quantity_type': 'l',
    'security_level': 1,
    'code': sample_code
}

sample_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'code': sample_code
}


def create_sample(client):
    response = client.post(sample_resource_route, json=sample_data, headers=sample_headers)
    return response


def prepare_sample_test(client):
    create_user(client)
    create_box(client)
    create_theme(client)
    create_quantity_type(client)
    create_security_level(client)
    create_sample(client)


"""
# *********************************************
# ***                                       ***
# ***  HELPER FUNCTIONS FOR PUBLICATION     ***
# ***                                       ***
# *********************************************
"""
publication_resource_route = '/publication'
publication_data = {
    'user': 1,
    'sample': 1,
    'sample_results': 'In progress',
    'publication_title': publication_code,
    'co_authors': 'Dr Gilbert'
}

publication_updated_data = {
    'user': 1,
    'sample': 1,
    'sample_results': 'Complete',  # <-- updated value
    'publication_title': publication_code,
    'co_authors': 'Dr Gilbert'
}

publication_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'title': publication_code
}


def create_publication(client):
    response = client.post(publication_resource_route, json=publication_data, headers=publication_headers)
    return response


def prepare_publication_test(client):
    create_user(client)
    create_theme(client)
    create_sample(client)
    create_publication(client)


"""
# *********************************************
# ***                                       ***
# ***  HELPER FUNCTIONS FOR HOUSE DATA      ***
# ***                                       ***
# *********************************************
"""
house_data_data = {
    'code': house_data_code,
    'user': 1,
    'education': 'Tertiary',
    'employment': 'Formal',
    'marital_status': 'Married',
    'people': 3,
    'children': 1,
    'animals': 5,
    'economic_activity': 'farming',
    'type_of_animals': 'cattle',
    'farming_activities': 'cattle farming',
    'social_economic_data': 'Data set 02'
}

house_data_updated_data = {
    'code': house_data_code,
    'user': 1,
    'education': 'Tertiary',
    'employment': 'Formal',
    'marital_status': 'Married',
    'people': 3,
    'children': '1',
    'animals': '5',
    'economic_activity': 'farming',
    'type_of_animals': 'cattle',
    'farming_activities': 'cattle farming',
    'social_economic_data': 'Data set 020'  # <-- updated value
}

house_data_headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'code': house_data_code
}


def create_house_data(client):
    create_user(client)
    response = client.post('/house-data', json=house_data_data, headers=house_data_headers)
    return response
