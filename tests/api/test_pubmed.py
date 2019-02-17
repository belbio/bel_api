import requests
import pytest

from bel.Config import config

api_url = config['bel_api']['servers']['api_url']


@pytest.mark.apitests
def test_pubmed_1():
    params = {'pubmed_only': True}
    r = requests.get(f'{api_url}/text/pubmed/19894120', params=params)
    assert r.status_code == 200
    body = r.json()

    assert body['pmid'] == '19894120'


@pytest.mark.apitests
def test_pubmed_2():
    params = {'pubmed_only': True}
    r = requests.get(f'{api_url}/text/pubmed/11035810', params=params)
    assert r.status_code == 200
    body = r.json()

    assert body['pmid'] == '11035810'
