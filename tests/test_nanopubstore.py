#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Usage:  program.py <customer>

"""
import requests
import json
import time

import bel.nanopub.nanopubstore as nanopubstore
import bel.setup_logging
import logging

bel.setup_logging.setup_logging()
log = logging.getLogger('root')

local_nano_api = 'http://nanopubstore.belapi.test'
plm_nano_api = 'https://nanopubstore.plm.biodati.com'


def load_nanopubs():

    if 0:
        params = {'max': 100000}
        r = requests.get(f'{plm_nano_api}/nanopubs', params=params)
        print(f'Downloading {r.status_code}')
        nanopubs = r.json()

        with open('nanopubs.json', 'w') as f:
            json.dump(nanopubs, f, indent=4)
    else:
        with open('nanopubs.json', 'r') as f:
            nanopubs = json.load(f)

    # Purge from Local!!!!
    # Logical delete first
    params = {'purge': 0, 'areyousure': 'yesiam'}
    r = requests.delete(f'{local_nano_api}/nanopubs', params=params)
    print(f'Logical delete all nanopubs {r.status_code}')
    # Then purge the logically deleted nanopubs
    params = {'purge': 1, 'areyousure': 'yesiam'}
    requests.delete(f'{local_nano_api}/nanopubs', params=params)
    print(f'Purge {r.status_code}')

    r = requests.get(f'{local_nano_api}/nanopubs/endpointstatus')
    print(f'Count of LocalDev nanopubs after purge: {r.json()}')

    r = requests.get(f'{local_nano_api}/search/resetindex')
    print(f'Resetting index {r.status_code}')

    count = 0
    setsize = 10
    headers = {'Content-Type': 'application/json'}
    nanopub_set = []
    for nanopub in nanopubs:
        count += 1
        nanopub_set.append(nanopub)
        if count % setsize == 0:
            pre_start_dt = nanopubstore.get_nanopubstore_start_dt(local_nano_api)

            print(f'Pre_start_dt {pre_start_dt}')

            r = requests.post('http://belapi.test/v1/tasks/pipeline')
            print(f'Kicking pipeline {r.status_code}')

            if r.status_code == 200:
                submitted_cnt = r.json()['submitted_cnt']
            else:
                submitted_cnt = 0

            post_start_dt = nanopubstore.get_nanopubstore_start_dt(local_nano_api)
            print(f'Pre-start_dt: {pre_start_dt}  Post-start_dt: {post_start_dt}  submitted_cnt: {submitted_cnt}')
            time.sleep(5)
            r = requests.post(f'{local_nano_api}/nanopubs/importmany', headers=headers, data=json.dumps(nanopub_set))
            print(f'Uploading {setsize} nanopubs: status={r.status_code}')
            nanopub_set = []

    r = requests.get(f'{local_nano_api}/nanopubs/endpointstatus')
    print(f'Count of LocalDev nanopubs: {r.json()}')

    r = requests.get(f'{local_nano_api}/search/count')
    print(f'Count of LocalDev nanopubs in search: {r.json()}')


def main():
    load_nanopubs()


if __name__ == '__main__':
    main()

