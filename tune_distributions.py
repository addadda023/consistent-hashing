from hashring import ConsistentHashing
import collections
import random
import math
import csv


def std_dev(population):
    mean = sum(population) / len(population)
    return math.sqrt(sum(pow(n - mean, 2) for n in population) / len(population))


def create_hash_ring(weight, num_nodes):
    """Returns instantiated hash ring object"""
    ring = ConsistentHashing(weight=weight)
    for index in range(1, num_nodes + 1):
        ring.add_node(node_name='node_name{}'.format(index), node='node{}'.format(index))

    return ring


def get_distributions(weight=100, num_nodes=20, num_hits=10000):
    """Returns standard deviation of requests served by each node given the number of replicas,
    number of nodes and number of requests."""
    # Is hash ring producing uniformly random distribution keys distributed among servers?
    ring = create_hash_ring(weight=weight, num_nodes=num_nodes)

    num_values = 10000
    distributions = collections.defaultdict(int)
    for index in range(num_hits):
        key = str(random.randint(1, num_values))
        node = ring.get_node(key)
        distributions[node] += 1

    standard_dev = std_dev(distributions.values())
    return standard_dev


def tune_request_distributions(num_weights):
    standard_dev = {}
    print('Number of servers: {}'.format(20))
    print('Number of requests: {}'.format(10000))

    for weight in range(num_weights):
        std_dev = get_distributions(weight + 1, num_nodes=20, num_hits=10000)
        # print('Number of replicas: {}, standard deviations of requests served: {}'.format(weight + 1, std_dev))
        standard_dev[weight] = std_dev

    with open('static/requests_tune.csv', 'w') as f:
        writer = csv.writer(f)
        for weight, std_dev in standard_dev.items():
            writer.writerow([weight+1, std_dev])


tune_request_distributions(num_weights=200)



