import base64
import jwt
from . import config

key_name = 'KEY'


def get_salt():
    salt = '00' + config.read_config().get("salt", '')
    return base64.decodebytes(salt.encode('utf-8'))


def decode(cipher: str):
    return jwt.decode(cipher, get_salt(), algorithms='HS256', options={"verify_signature": False}).get(key_name)


def enconde(plain: str):
    return jwt.encode({key_name: plain}, get_salt(), algorithm='HS512')
