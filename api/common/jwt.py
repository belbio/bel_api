import jwt
import os
from datetime import datetime, timedelta

from bel.Config import config

import logging
log = logging.getLogger(__name__)

jwt_secret_key = os.getenv('JWT_SECRET', None)


def create_token():
    """Create JWT token using Auth0 Secret Key"""

    payload = {"name": "belapi"}
    token = jwt.encode(payload, jwt_secret_key, algorithm='HS256')
    return token


def jwt_create(userid, payload, expiration=None):
    """Create a JSON Web Token
        payload: dictionary to be added to JWT
        expiration:  number of seconds from now to expire token -- defaults to 3600 seconds

    """

    jwt_algorithm = 'HS256'

    if expiration:
        exp = datetime.utcnow() + timedelta(seconds=expiration)
    else:
        exp = datetime.utcnow() + timedelta(seconds=3600)

    additional_payload = {
        'sub': userid,
        'exp': exp,
        'iat': datetime.utcnow(),
    }

    log.debug('UserId: ', userid, ' Payload: ', payload)

    payload.update(additional_payload)
    token = jwt.encode(payload, config['secrets']['bel_api']['shared_secret'], algorithm=jwt_algorithm)

    return token.decode('utf-8')


def jwt_validate(token):
    """Validates JSON Web Token
        Returns:
            valid:          boolean - true if valid token
            token_payload:  dict of token payload
    """
    try:
        jwt.decode(token, config['secrets']['bel_api']['shared_secret'], algorithm=jwt_algorithm)
        return True
    except Exception as e:
        return False


def jwt_extract(token):
    log.debug('In JWT Extract')
    try:
        return jwt.decode(token, config['secrets']['bel_api']['shared_secret'], algorithm=jwt_algorithm), ''
    except jwt.ExpiredSignatureError:
        log.debug('JWT expired')
        return None, 'JWT expired'
    except Exception as e:
        log.debug('JWT extraction error ', e)
        return None, e
