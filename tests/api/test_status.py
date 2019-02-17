import requests
import pytest

# from common.jwt import jwt_create

from bel.Config import config

api_url = config['bel_api']['servers']['api_url']

userid = 1
payload = {}
# token = jwt_create(userid, payload)


@pytest.mark.apitests
def test_simple_status():
    r = requests.get(f'{api_url}/simple_status', params=None)
    assert r.status_code == 200


@pytest.mark.apitests
def test_status():

    r = requests.get(f'{api_url}/status')
    body = r.json()

    assert r.status_code == 200
    assert body['api_version'] >= '0.2.0'
    assert body.get('api_settings', False)


@pytest.mark.apitests
@pytest.mark.skip(reason="Skip for now")
def test_status_authenticated():
    # r = requests.get(f'{api_url}/status', params=None)
    # assert r.status_code == 401

    token = None
    headers = {'Authorization': f'JWT {token}'}
    r = requests.get(f'{api_url}/status', headers=headers)
    body = r.json()

    assert r.status_code == 200
    assert body['api_version'] >= '0.2.0'
    assert body.get('api_settings', False)

