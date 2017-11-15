import requests
import pytest
from Config import config
from common.authentication import jwt_create

api_url = config['docker_test_api_url']

userid = 1
payload = {}
token = jwt_create(userid, payload)


@pytest.mark.apitests
def test_simple_status():
    r = requests.get(f'{api_url}/simple_status', params=None)
    assert r.status_code == 200


@pytest.mark.apitests
def test_status():
    r = requests.get(f'{api_url}/status', params=None)
    assert r.status_code == 401

    headers = {'Authorization': f'JWT {token}'}
    r = requests.get(f'{api_url}/status', headers=headers)
    assert r.status_code == 200
