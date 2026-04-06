# Cache System Design - LRU
# Design a Least Recently Used (LRU) Cache Data Structure

# Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.
# https://en.wikipedia.org/wiki/Cache_replacement_policies#LRU
# The functions get and put must each run in O(1) average time complexity.

"""
Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the LRUCache class:

LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
int get(int key) Return the value of the key if the key exists, otherwise return -1.
void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.
The functions get and put must each run in O(1) average time complexity.

Example 1:

Input
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
Output
[null, null, null, 1, null, -1, null, -1, 3, 4]

Explanation
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // return 1
lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
lRUCache.get(2);    // returns -1 (not found)
lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
lRUCache.get(1);    // return -1 (not found)
lRUCache.get(3);    // return 3
lRUCache.get(4);    // return 4

Constraints:

1 <= capacity <= 3000
0 <= key <= 104
0 <= value <= 105
At most 2 * 105 calls will be made to get and put.
"""

# Data structure
"""
1. Use a hash map key -> node (fast lookup).
2. Use a doubly linked list that stores nodes in most-recently-used → least-recently-used order.

head = MRU
tail = LRU

3. moving a node to the front is O(1)
4. removing the LRU node from the back is O(1)
"""

# Key idea
"""
1. Every key in the cache has exactly one node in the linked list.
2. The linked list order represents recency.
3. After any get(key) that hits, that key becomes most recently used 
    (move to head).
4. After any put(key,value), that key becomes most recently used.
4. Advisable to use Dummy Nodes for head and tail to overcome edge cases
6. If size exceeds capacity, evict the tail.prev (least recently used).
"""

class Node:
    __slots__ = ("key", "val", "prev", "next")
    def __init__(self, key: int, val: int):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUcache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map: dict[int, Node] = {} # This maps key -> Node
        # Use Dummy Nodes for head and tail to overcome edge cases
        self.head = Node(-1, -1) # MRU side of linked list (after head)
        self.tail = Node(-1, -1) # LRU side of linked list (before tail)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    # cache doubly linked list helper functions
    def _remove_node(self, node: Node) -> Node:
        prev_node, next_node = node.prev, node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        node.prev = node.next = None
        return node
    
    def _add_to_front(self, node: Node) -> Node:
        # Insert node just after dummy head
        current_mru = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = current_mru
        current_mru.prev = node
        return node

    def _move_node_to_front(self, node: Node) -> None:
        self._remove_node(node)
        self._add_to_front(node)
        return node
    
    def _pop_lru(self) -> Node:
        lru_node = self.tail.prev
        self._remove_node(lru_node)
        return lru_node
    
    # cache API
    def get(self, key: int) -> int:
        node = self.map.get(key)

        if not node:
            return -1
        
        self._move_node_to_front(node)
        return node.val
    
    def put(self, key: int, value: int) -> None:
        node = self.map.get(key)

        if node:
            node.val = value
            self.map[key] = node
            self._move_node_to_front(node)
            return None

        new_node = Node(key, value)
        self.map[key] = new_node
        self._add_to_front(new_node)

        if len(self.map) > self.capacity:
            lru_node = self._pop_lru() # Remove from linked list
            del self.map[lru_node] # Remove key-value from Hash map
        return None

# Complexities
"""
get: O(1) on average (hash lookup + O(1) list operations)
put: O(1) on average (hash lookup/insert + O(1) list operations + 
        optional O(1) eviction)
Space: O(capacity)
"""
