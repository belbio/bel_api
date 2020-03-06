import yaml
import os
import sys

import structlog

log = structlog.getLogger(__name__)

possible_env_variables = ["CORS_ORIGINS"]

conf_fn = os.environ.get("CONF_FN")

# TODO - figure out how to make this work via pytest.ini envs
# conf_fn = "/Users/william/studio/dev/userstore/tests/testdata/userstore.yml"


def get_config():

    if not os.path.isfile(conf_fn):
        log.error("Please add userstore config (yml) location to environment var: CONF_FN")
        sys.exit("Please add userstore config (yml) location to environment var: CONF_FN")

    with open(conf_fn, "r") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)

    # Override config with env vars
    for env_key in possible_env_variables:
        if env_key in os.environ:
            config[env_key.lower()] = os.environ.get(env_key)

    if config["cors_origins"]:
        config["cors_origins"] = config["cors_origins"].split(",")

    return config


config = get_config()
