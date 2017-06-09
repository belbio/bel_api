from Config import config

import itsdangerous
from passlib.hash import sha256_crypt
import jwt

from datetime import datetime, timedelta
import logging

logger = logging.getLogger(name='root.common.authentication')
jwt_algorithm = 'HS256'


# TODO Remember me functionality: use a timedtoken from itsdangerous and storing using a secure cookie
#          might just have the REST API Falcon middleware get a new token with an hour more if it's expired so
#          that a user's session doesn't get killed

def jwt_create(userid, payload, expiration=None):
    """Create a JSON Web Token
        payload: dictionary to be added to JWT
        expiration:  number of seconds from now to expire token -- defaults to config['token_expiration_seconds']

    """

    if expiration:
        exp = datetime.utcnow() + timedelta(seconds=expiration)
    else:
        exp = datetime.utcnow() + timedelta(seconds=config['token_expiration_seconds'])

    additional_payload = {
        'sub': userid,
        'exp': exp,
        'iat': datetime.utcnow(),
    }

    logger.debug('UserId: ', userid, ' Payload: ', payload)

    payload.update(additional_payload)
    token = jwt.encode(payload, config['token_secret'], algorithm=jwt_algorithm)

    return token.decode('utf-8')


# TODO  Might want to refresh token for another hour if it's within 10 minutes or so of expiration
#          to allow users to keep a working session going

def jwt_validate(token):
    """Validates JSON Web Token
        Returns:
            valid:          boolean - true if valid token
            token_payload:  dict of token payload
    """
    try:
        jwt.decode(token, config['token_secret'], algorithm=jwt_algorithm)
        return True
    except:
        return False


def jwt_extract(token):
    logger.debug('In JWT Extract')
    try:
        return jwt.decode(token, config['token_secret'], algorithm=jwt_algorithm), ''
    except jwt.ExpiredSignatureError:
        logger.debug('JWT expired')
        return None, 'JWT expired'
    except Exception as e:
        logger.debug('JWT extraction error ', e)
        return None, e


def encrypt_password(password):
    return sha256_crypt.encrypt(password)


def verify_password(password, password_hash):
    return sha256_crypt.verify(password, password_hash)
