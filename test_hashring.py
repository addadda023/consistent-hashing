import unittest
from hashring import ConsistentHashing


class TestConsistentHashing(unittest.TestCase):

    def create_hash_ring(self, weight, num_nodes):
        """Returns instantiated hash ring object"""
        ring = ConsistentHashing(weight=weight)
        for index in range(1, num_nodes + 1):
            ring.add_node(node_name='node_name{}'.format(index), node='node{}'.format(index))

        return ring

    def test_add_node(self):
        ring = self.create_hash_ring(weight=5, num_nodes=10)
        # Before adding node
        self.assertEqual(ring.get_node('2'), 'node5')
        # Add node
        ring.add_node(node_name='node_name{}'.format(11), node='node{}'.format(11))
        # After adding new node
        self.assertEqual(ring.get_node('2'), 'node5')

    def test_remove_node(self):
        ring = self.create_hash_ring(weight=5, num_nodes=10)
        # Before removing node
        self.assertEqual(ring.get_node('2'), 'node5')
        ring.remove_node('node_name5')
        # After removing node, key 2 should be served by node9
        self.assertEqual(ring.get_node('2'), 'node9')



