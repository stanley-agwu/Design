# Cache System Design - LFU
# Design a Least Frequently Used (LFU) Cache Data Structure

# Design and implement a data structure for a Least Frequently Used (LFU) cache.
# https://en.wikipedia.org/wiki/Least_frequently_used
# The functions get and put must each run in O(1) average time complexity.


# Key Idea
"""
To get O(1) average for both get and put with LFU + LRU tie-break, 
the standard design is:

1. key -> node hash map (find/update in O(1))
2. freq -> doubly linked list of nodes (each list is LRU order within that frequency)
3. Track minFreq (the smallest frequency currently present)

When a key is accessed (by get or put on an existing key):

1. Remove node from its current frequency list.
2. Increment its frequency.
3. Add it to the front (most-recent) of the new frequency list.
4. If the old list became empty and it was minFreq, increment minFreq.

When inserting a new key and cache is full:
Evict from freq = minFreq list, specifically the tail (least recently used among the least frequent).
"""

class Node:
    __slots__ = ("key", "val", "freq", "prev", "next")

    def __init__(self, key: int, val: int):
        self.key = key
        self.val = val
        self.freq = 1
        self.prev = None
        self.next = None


class DLL:
    """
    Doubly-linked list with sentinels.
    Head side = most recent
    Tail side = least recent
    """
    __slots__ = ("head", "tail", "size")

    def __init__(self):
        # Use Dummy Nodes for head and tail to overcome edge cases
        self.head = Node(-1, -1)
        self.tail = Node(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def append_left(self, node: Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node
        self.size += 1

    def remove(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node.next = None
        self.size -= 1

    def pop_right(self) -> Node | None:
        if self.size == 0:
            return None
        node = self.tail.prev
        self.remove(node)
        return node


class LFUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.size = 0

        self.min_freq = 0
        self.keyToNode: dict[int, Node] = {}
        self.freqToDLL: dict[int, DLL] = {}

    def _touch(self, node: Node) -> None:
        """Increase node's freq and move it to correct freq list (most recent)."""
        old_freq = node.freq
        old_list = self.freqToDLL[old_freq]
        old_list.remove(node)

        # if this node was the last one in minFreq list, bump minFreq
        if old_freq == self.min_freq and old_list.size == 0:
            self.min_freq += 1

        node.freq += 1
        new_freq = node.freq
        new_list = self.freqToDLL.get(new_freq)
        if new_list is None:
            new_list = DLL()
            self.freqToDLL[new_freq] = new_list
        new_list.append_left(node)

    def get(self, key: int) -> int:
        node = self.keyToNode.get(key)
        if node is None:
            return -1
        self._touch(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return

        node = self.keyToNode.get(key)
        if node is not None:
            node.val = value
            self._touch(node)
            return

        # need to insert a new key
        if self.size == self.cap:
            # evict LFU and LRU within that freq
            lfu_list = self.freqToDLL[self.min_freq]
            victim = lfu_list.pop_right()  # LRU among minFreq
            del self.keyToNode[victim.key]
            self.size -= 1

        new_node = Node(key, value)
        self.keyToNode[key] = new_node

        freq1 = self.freqToDLL.get(1)
        if freq1 is None:
            freq1 = DLL()
            self.freqToDLL[1] = freq1
        freq1.append_left(new_node)

        self.min_freq = 1
        self.size += 1

# Complexities
"""
get: hashmap lookup + remove/insert in two DLLs + a few integer 
        updates ⇒ O(1).
put: - existing key: same as get ⇒ O(1).
     - new key: maybe evict tail of minFreq list ⇒ O(1), then insert 
        into freq=1 list ⇒ O(1).
Space: O(capacity) nodes plus some frequency lists.
"""