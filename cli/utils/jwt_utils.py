import base64
import jwt
from . import config

salt = '00'+config.read_config().get("salt")
j_salt = base64.decodebytes(salt.encode('utf-8'))
key_name = 'KEY'


def decode(cipher: str):
    return jwt.decode(cipher, j_salt, algorithms='HS256', options={"verify_signature": False}).get(key_name)


def enconde(plain: str):
    return jwt.encode({key_name: plain}, j_salt, algorithm='HS512')

