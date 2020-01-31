from flask import json, request

from api import create_app as app


def test_get_user(client):
    response = client.get('/users')
    assert b'message' in response.data
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Users not found'

    elif response.status_code == 200:
        # check that the list is more than 1 item
        assert len(data['message']) >= 1

        # check that each element in the list contains; role, email and name(s)
        for item in range(len(data['message'])):
            assert data['message'][item]['email']
            assert data['message'][item]['first_name']
            assert data['message'][item]['last_name']
            assert data['message'][item]['role.name']


# todo: change the params to an admin user
def test_get_user_by_params(client):
    with app().test_request_context('/user?email=brittney71@gmail.com&deleted=false&role=8'):
        assert request.path == '/user'
        assert request.args['email'] == 'brittney71@gmail.com'
        assert request.args['deleted'] == 'false'
        assert request.args['role'] == '8'

    response = client.get('/user?email=brittney71@gmail.com&deleted=false&role=8')
    data = json.loads(response.data)

    if response.status_code == 404:
        assert data['message'] == 'Users not found'

    elif response.status_code == 200:
        assert data['message']['email'] == 'brittney71@gmail.com'
        assert data['message']['first_name']
        assert data['message']['last_name']
        assert data['message']['role.name']
