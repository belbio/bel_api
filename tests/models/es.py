from Config import config

import models.es as es

if config.server_type not in ['DEV', 'TEST']:
    print('Production server? Will not run tests unless config["server_type"] is DEV or TEST')
    assert False


def test_index_exists():
    assert 0
    result = es.index_exists('terms')
    print(result)

    assert False
