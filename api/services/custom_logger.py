import logging
from Config import config

# config['api_log_fn'] = 'api.log'
# config['log_level'] = 'DEBUG'


def setup_custom_logger(name):
    logger = logging.getLogger(name)

    stream_handler = logging.StreamHandler()
    # formatter = logging.Formatter(
    #     '[%(asctime)s] [%(name)s:%(module)s:%(lineno)d] [%(levelname)s] %(message)s')
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(filename)s->%(funcName)s:%(lineno)s] %(message)s')
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(config.api_log_fn)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(config.log_level)

    return logger
