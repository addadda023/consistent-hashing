from hashring import ConsistentHashing
import random
import string

base62 = string.ascii_uppercase + string.ascii_lowercase + '0123456789'


def create_empty_hash_ring(weight):
    """Returns instantiated empty hash ring object"""
    ring = ConsistentHashing(weight=weight)

    return ring


def create_key_value(key_len=6, value_len=10):
    key = ''.join(random.sample(base62, key_len))
    value = ''.join(random.sample(base62, value_len))
    return key,value
