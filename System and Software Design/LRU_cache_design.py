# Cache System Design - LRU
# Design a Least Recently Used (LRU) Cache Data Structure

# Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.
# https://en.wikipedia.org/wiki/Cache_replacement_policies#LRU
# The functions get and put must each run in O(1) average time complexity.


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
    
    def _add_to_front(self, node: Node) -> Node:
        # Insert node just after dummy head
        current_mru = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = current_mru
        current_mru.prev = node

    def _move_node_to_front(self, node: Node) -> None:
        self._remove_node(node)
        self._add_to_front(node)
    
    def _pop_lru(self) -> Node:
        lru_node = self.tail.prev
        self._remove_node(lru_node.key)
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
