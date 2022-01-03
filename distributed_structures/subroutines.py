from hashlib import new as hash_type
from json import dumps
from distributed_structures.common import types
from os import environ

def hash_string(data):
    hash_fn = environ.get('DISTRIBUTED_STRUCTURES_HASH_FN')
    if not hash_fn:
        hash_fn = 'md5'

    hasher = hash_type(hash_fn)
    hasher.update(data.encode())
    return hasher.hexdigest()

def type_to_string(t):
    for tp in types:
        if t == types[tp]:
            return tp