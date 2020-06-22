![](https://github.com/addadda023/consistent-hashing/workflows/Python%20application/badge.svg)

# Consistent Hashing

Distributed Hash Table is one of the fundamental components used in distributed systems.

Hash Tables need a key, a value, and a hash function where hash function maps the key to a location where the value is stored.

`index = hash_function(key)`

Suppose we are designing a distributed caching system. Given ‘n’ cache servers, an intuitive hash
 function would be ‘key % n’. It is simple and commonly used. But it has two major drawbacks:

It is NOT horizontally scalable. Whenever a new cache host is added to the system, all existing mappings are broken.
 It will be a pain point in maintenance if the caching system contains lots of data. 
 Practically, it becomes difficult to schedule a downtime to update all caching mappings.
It may NOT be load balanced, especially for non-uniformly distributed data. 
In practice, it can be easily assumed that the data will not be distributed uniformly. 
For the caching system, it translates into some caches becoming hot and saturated while the others idle and are almost empty.
In such situations, consistent hashing is a good way to improve the caching system.

## What is Consistent Hashing? 
Consistent hashing is a very useful strategy for distributed caching systems and DHTs. 
It allows us to distribute data across a cluster in such a way that will minimize 
reorganization when nodes are added or removed. Hence, the caching system will be easier to scale up or scale down.

In Consistent Hashing, when the hash table is resized (e.g. a new cache host is added to the system), 
only ‘k/n’ keys need to be remapped where ‘k’ is the total number of keys and ‘n’ is the total number of servers.
 Recall that in a caching system using the ‘mod’ as the hash function, all keys need to be remapped.

In Consistent Hashing, objects are mapped to the same host if possible. When a host is removed from the system,
 the objects on that host are shared by other hosts; when a new host is added, it takes its share from a few hosts without touching other’s shares.

## How does it work? 
As a typical hash function, consistent hashing maps a key to an integer. Suppose the output of the hash function is in the range of [0, 256]. Imagine that the integers in the range are placed on a ring such that the values are wrapped around.

Here’s how consistent hashing works:

* Given a list of cache servers, hash them to integers in the range.
* To map a key to a server:
  * Hash it to a single integer.
  * Move clockwise on the ring until finding the first cache it encounters.
  * That cache is the one that contains the key. 
 
 
![Hash Ring](/static/hash_ring.png)


To add a new server, say S<sub>N-1</sub>, keys that were originally residing at S<sub>2</sub> will be split. 
Some of them will be shifted to S<sub>N-1</sub>, while other keys will not be touched.

To remove a server or, if a server fails, say S<sub>3</sub>, all keys that were originally mapped 
to S<sub>3</sub> will fall into S<sub>2</sub>, and only those keys need to be moved to 
S<sub>2</sub>; other keys will not be affected.

For load balancing, as we discussed in the beginning, the real data is essentially randomly
 distributed and thus may not be uniform. It may make the keys on caches unbalanced.

To handle this issue, we add “virtual replicas” for caches. TInstead of mapping each
 cache to a single point on the ring, we map it to multiple points on the
  ring, i.e. replicas. This way, each cache is associated with multiple portions of the ring.

If the hash function “mixes well,” as the number of replicas increases, the keys 
will be more balanced. This is 
implemented by **weight** parameter when initializing hash ring.

## Usage

```python
from hashring import ConsistentHashing

# create a consistent hash ring with 5 replicas for each node(server)
ring = ConsistentHashing(weight=5)

# you can use whatever node you want, such as Redis clients
import redis
ring.add_node(node_name='node1', node=redis.StrictRedis(host='host1'))
ring.add_node(node_name='node2', node=redis.StructRedis(host='host2'))

client = ring.get_node('some_node_name')
data = client.get('some key')
```

## How randomly uniformly distributed are requests? 
Below chart was generated using:
* 20 servers.
* 10,000 total requests.
* 1 to 200 virtual replicas for each of the 20 servers. 

Increasing number of replicas generally helps to randomly distribute requests but there is diminishing returns after certain threshold.

![](/static/std_dev_vs_replicas.png)
