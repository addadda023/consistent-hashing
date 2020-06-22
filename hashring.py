import hashlib
import bisect


class ConsistentHashing:
    def __init__(self, weight=10):
        """ConsistentHashing object.
        :param weight: number of replicas of each node"""
        self.weight = weight
        self._keys = []
        self._nodes = {}

    @staticmethod
    def _hash(key):
        """Generate hash value using given key"""
        return hashlib.md5(key.encode('utf-8')).hexdigest()

    def _node_list(self, node_name):
        """Given node_name, return all replicas"""
        return [self._hash('{}+{}'.format(node_name, index))
                for index in range(self.weight)]

    def add_node(self, node_name, node):
        """Add a node using its name. Given node name is hashed in the ring."""
        for hash_ in self._node_list(node_name):
            if hash_ in self._nodes:
                raise ValueError('Node name {} is already present'.format(node_name))
            self._nodes[hash_] = node
            # Insert hash to keys
            bisect.insort(self._keys, hash_)

    def remove_node(self, node_name):
        """Remove all nodes of a given node name from the ring"""
        for hash_ in self._node_list(node_name):
            if hash_ in self._nodes:
                self._nodes.pop(hash_, None)
                index = bisect.bisect_left(self._keys, hash_)
                del self._keys[index]
            else:
                raise KeyError('Node name {} not present in hash ring'.format(node_name))

    def get_node(self, key):
        """Using provided key, return it's node.
        Node replica with a hash value nearest than
        that of the given key is returned."""
        hash_ = self._hash(key)
        index = bisect.bisect(self._keys, hash_)
        if index == len(self._keys):
            index = 0
        return self._nodes[self._keys[index]]



