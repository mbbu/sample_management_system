import datetime
import decimal

import pytest

from api import create_app as app
from api.tests.unittest.utils_for_tests import theme_resource_route, theme_data, prepare_user_test, USER_DATA, \
    prepare_sample_test, sample_code, sample_data
from api.utils import non_empty_string, standard_non_empty_string, format_and_lower_str, non_empty_int, \
    format_str_to_date, get_active_users, get_user_by_email, get_users_by_role, get_users_by_status, \
    get_deactivated_user, log_in_user_jwt, get_sample_by_code


def test_non_empty_string():
    with pytest.raises(ValueError):
        non_empty_string("")
        non_empty_string("   ")
        assert ValueError

    s = non_empty_string("String")
    assert s == 'String'


def test_standard_non_empty_string():
    with pytest.raises(ValueError):
        standard_non_empty_string("")
        standard_non_empty_string("   ")
        assert ValueError

    s = standard_non_empty_string("STRING")
    assert s == 'string'


def test_format_and_lower_str():
    s = format_and_lower_str("String")
    q = format_and_lower_str("STRING")
    r = format_and_lower_str("STriNG")
    t = format_and_lower_str("stRInG")

    assert s == q == r == t == 'string'


def test_non_empty_int():
    with pytest.raises(ValueError):
        non_empty_int("")
        non_empty_int(100.00)
        assert ValueError

    i = non_empty_int(100)
    assert i == 100


def test_format_str_to_date():
    with pytest.raises(ValueError):
        format_str_to_date("")
        format_str_to_date("01-01-01")

        assert ValueError

    d = "2020-01-01 12:00"
    d = format_str_to_date(d)

    assert isinstance(d, datetime.date)


def test_prepare_db(client):
    response = client.post(theme_resource_route, json=theme_data)
    assert response.status_code == 401


def test_get_active_users(client):
    prepare_user_test(client)
    users = get_active_users()

    assert users
    assert type(users) == list
    assert len(users) >= 1


def test_get_user_by_email(client):
    prepare_user_test(client)
    user = get_user_by_email(USER_DATA['email'])

    assert user
    assert user.email == USER_DATA['email']
    assert user.first_name == USER_DATA['first_name']
    assert user.last_name == USER_DATA['last_name']


def test_get_users_by_role(client):
    prepare_user_test(client)
    users = get_users_by_role(USER_DATA['role'])

    assert users
    assert type(users) == list
    assert len(users) >= 1


def test_get_users_by_status(client):
    prepare_user_test(client)
    users = get_users_by_status(False)

    assert users
    assert type(users) == list
    assert len(users) >= 1


def test_get_deactivated_user(client):
    prepare_user_test(client)
    users = get_deactivated_user(USER_DATA['email'])

    assert users is None


def test_log_in_user_jwt(client):
    prepare_user_test(client)
    user = get_user_by_email(USER_DATA['email'])

    with app().test_request_context():
        response = log_in_user_jwt(user)

    assert response['access_token']
    assert response['refresh_token']


def test_get_samples_by_code(client):
    prepare_sample_test(client)
    sample = get_sample_by_code(format_and_lower_str(sample_code))

    assert sample
    assert sample.theme.id == sample_data['theme']
    assert sample.user.id == sample_data['user']
    assert sample.box.id == sample_data['box']
    assert sample.animal_species == sample_data['animal_species']
    assert sample.sample_type == sample_data['sample_type']
    assert sample.sample_description == sample_data['sample_description']
    assert sample.location_collected == sample_data['location_collected']
    assert sample.project == sample_data['project']
    assert sample.project_owner == sample_data['project_owner']
    assert sample.retention_period == sample_data['retention_period']
    assert sample.barcode == sample_data['barcode']
    assert sample.analysis == sample_data['analysis']
    assert sample.temperature == decimal.Decimal(sample_data['temperature'])
    assert sample.amount == sample_data['amount']
    assert sample.quantity.id == sample_data['quantity_type']
    assert sample.bio_hazard_level == sample_data['bio_hazard_level']
    assert sample.code == format_and_lower_str(sample_code)
