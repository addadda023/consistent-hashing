from utils import create_empty_hash_ring, create_key_value
import random
import string
import redis
import logging
from hashring import ConsistentHashing

# log transport
logging.basicConfig(level=logging.INFO)

# connect to redis
r1 = redis.Redis(host='127.0.0.1', port=6379)
r2 = redis.Redis(host='127.0.0.1', port=7001)

# create hash ring
ring = create_empty_hash_ring(weight=10)
# add nodes to hash ring
ring.add_node(node_name='redis1', node=r1)
ring.add_node(node_name='redis2', node=r2)

# create key-value pairs
d = {}
for index in range(10):
    key, value = create_key_value()
    d[key] = value

# assign key-value pairs to servers in the hash ring
for key, value in d.items():
    client_name, client = ring.get_node(key)
    logging.info('Chose node {}'.format(client_name))
    # add to redis node
    client.set(key, value)

# read values
for key in list(d.keys()):
    _, client = ring.get_node(key)
    # print value
    print(key, client.get(key))


