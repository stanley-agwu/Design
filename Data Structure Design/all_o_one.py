# All O`one Data Structure


"""
Design a data structure to store the strings' count with the ability to 
return the strings with minimum and maximum counts.

Implement the AllOne class:

AllOne() Initializes the object of the data structure.
inc(String key) Increments the count of the string key by 1. If key does not 
    exist in the data structure, insert it with count 1.
dec(String key) Decrements the count of the string key by 1. If the count of key 
    is 0 after the decrement, remove it from the data structure. It is guaranteed 
    that key exists in the data structure before the decrement.
getMaxKey() Returns one of the keys with the maximal count. If no element exists, 
    return an empty string "".
getMinKey() Returns one of the keys with the minimum count. If no element exists, 
    return an empty string "".
Note that each function must run in O(1) average time complexity.

 

Example 1:

Input
["AllOne", "inc", "inc", "getMaxKey", "getMinKey", "inc", "getMaxKey", "getMinKey"]
[[], ["hello"], ["hello"], [], [], ["leet"], [], []]
Output
[null, null, null, "hello", "hello", null, "hello", "leet"]

Explanation
AllOne allOne = new AllOne();
allOne.inc("hello");
allOne.inc("hello");
allOne.getMaxKey(); // return "hello"
allOne.getMinKey(); // return "hello"
allOne.inc("leet");
allOne.getMaxKey(); // return "hello"
allOne.getMinKey(); // return "leet"
 

Constraints:

1 <= key.length <= 10
key consists of lowercase English letters.
It is guaranteed that for each call to dec, key is existing in the data structure.
At most 5 * 104 calls will be made to inc, dec, getMaxKey, and getMinKey.
"""

class Node:
    __slots__ = ("count", "keys", "prev", "next")

    def __init__(self, count: int):
        self.count = count
        self.keys = set()
        self.prev = None
        self.next = None


class AllOne:
    def __init__(self):
        self.head = Node(0)   # sentinel
        self.tail = Node(0)   # sentinel
        self.head.next = self.tail
        self.tail.prev = self.head
        self.where = {}  # key -> Node

    # ----- linked list helpers -----
    def _insert_after(self, node: Node, new_node: Node) -> None:
        nxt = node.next
        new_node.prev = node
        new_node.next = nxt
        node.next = new_node
        nxt.prev = new_node

    def _remove_node(self, node: Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = node.next = None

    # ----- API -----
    def inc(self, key: str) -> None:
        if key not in self.where:
            # place into count=1 bucket right after head
            first = self.head.next
            if first is self.tail or first.count != 1:
                one = Node(1)
                self._insert_after(self.head, one)
                first = one
            first.keys.add(key)
            self.where[key] = first
            return

        cur = self.where[key]
        nxt = cur.next
        target_count = cur.count + 1

        if nxt is self.tail or nxt.count != target_count:
            new_bucket = Node(target_count)
            self._insert_after(cur, new_bucket)
            nxt = new_bucket

        # move key
        cur.keys.remove(key)
        nxt.keys.add(key)
        self.where[key] = nxt

        if not cur.keys:
            self._remove_node(cur)

    def dec(self, key: str) -> None:
        cur = self.where[key]
        if cur.count == 1:
            # remove key entirely
            cur.keys.remove(key)
            del self.where[key]
            if not cur.keys:
                self._remove_node(cur)
            return

        prev = cur.prev
        target_count = cur.count - 1

        if prev is self.head or prev.count != target_count:
            new_bucket = Node(target_count)
            self._insert_after(prev, new_bucket)  # insert between prev and cur
            prev = new_bucket

        # move key
        cur.keys.remove(key)
        prev.keys.add(key)
        self.where[key] = prev

        if not cur.keys:
            self._remove_node(cur)

    def get_max_key(self) -> str:
        if self.tail.prev is self.head:
            return ""
        return next(iter(self.tail.prev.keys))

    def get_min_key(self) -> str:
        if self.head.next is self.tail:
            return ""
        return next(iter(self.head.next.keys))
    
# O(1) - Time complexity - for: inc, dec, get_max_key, get_min_key
# O(n) - Space complexity