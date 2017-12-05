from Config import config

import models.es as es

if config.servers.server_type not in ['DEV', 'TEST']:
    print('Production server? Will not run tests unless config.servers.server_type is DEV or TEST')
    assert False


def test_index_exists():
    result = es.index_exists('terms')
    print(result)

    assert False
