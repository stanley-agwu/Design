# Design a Hash Set

"""
Design a HashSet without using any built-in hash table libraries.

Implement MyHashSet class:

void add(key) Inserts the value key into the HashSet.
bool contains(key) Returns whether the value key exists in the HashSet or not.
void remove(key) Removes the value key in the HashSet. If key does not exist 
    in the HashSet, do nothing.
 

Example 1:

Input
["MyHashSet", "add", "add", "contains", "contains", "add", "contains", "remove", "contains"]
[[], [1], [2], [1], [3], [2], [2], [2], [2]]
Output
[null, null, null, true, false, null, true, null, false]

Explanation
MyHashSet myHashSet = new MyHashSet();
myHashSet.add(1);      // set = [1]
myHashSet.add(2);      // set = [1, 2]
myHashSet.contains(1); // return True
myHashSet.contains(3); // return False, (not found)
myHashSet.add(2);      // set = [1, 2]
myHashSet.contains(2); // return True
myHashSet.remove(2);   // set = [1]
myHashSet.contains(2); // return False, (already removed)
 

Constraints:

0 <= key <= 106
At most 104 calls will be made to add, remove, and contains.
"""

# Idea
"""
A clean way to design this is with separate chaining:
1. Use an array of buckets
2. Each bucket stores keys that hash to that index

For each operation:
1. compute bucket index with key % size
2. scan that bucket

Because keys are up to 10^6 and there are only 10^4 operations, this works very well.

A HashSet only needs to support:
1. add(key)
2. remove(key)
3. contains(key)

We can choose a fixed number of buckets, say a prime like 1009, to reduce collisions.
"""

class MyHashSet:

    def __init__(self):
        self.size = 1009
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        return key % self.size

    def add(self, key: int) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]

        if key not in bucket:
            bucket.append(key)

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, k in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return

    def contains(self, key: int) -> bool:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        return key in bucket

# Time complexity
"""
Let k be the number of elements in one bucket.
add → O(k)
remove → O(k)
contains → O(k)
"""

# Space complexity:
# Let n = number of stored keys, b = number of buckets
# O(n + b)
