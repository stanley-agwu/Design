# Zigzag Iterator

"""
Given two vectors of integers v1 and v2, implement an iterator to return their 
elements alternately.

Implement the ZigzagIterator class:

ZigzagIterator(List<int> v1, List<int> v2) initializes the object with the two 
    vectors v1 and v2.
boolean hasNext() returns true if the iterator still has elements, and false otherwise.
int next() returns the current element of the iterator and moves the iterator 
    to the next element.

Example 1:

Input: v1 = [1,2], v2 = [3,4,5,6]
Output: [1,3,2,4,5,6]
Explanation: By calling next repeatedly until hasNext returns false, the order 
of elements returned by next should be: [1,3,2,4,5,6].
Example 2:

Input: v1 = [1], v2 = []
Output: [1]
Example 3:

Input: v1 = [], v2 = [1]
Output: [1]

Constraints:

0 <= v1.length, v2.length <= 1000
1 <= v1.length + v2.length <= 2000
-231 <= v1[i], v2[i] <= 231 - 1
 

Follow up: What if you are given k vectors? How well can your code be extended 
to such cases?

Clarification for the follow-up question:

The "Zigzag" order is not clearly defined and is ambiguous for k > 2 cases. 
If "Zigzag" does not look right to you, replace "Zigzag" with "Cyclic".

Follow-up Example:

Input: v1 = [1,2,3], v2 = [4,5,6,7], v3 = [8,9]
Output: [1,4,8,2,5,9,3,6,7]
"""

from collections import deque
from typing import List


class ZigzagIterator:
    def __init__(self, v1: List[int], v2: List[int]):
        self.queue = deque()

        if v1:
            self.queue.append((v1, 0))
        if v2:
            self.queue.append((v2, 0))

    def next(self) -> int:
        vec, idx = self.queue.popleft()
        value = vec[idx]

        if idx + 1 < len(vec):
            self.queue.append((vec, idx + 1))

        return value

    def has_next(self) -> bool:
        return len(self.queue) > 0
    
# Complexity Analysis
"""
Time Complexity: O(1) for next() and has_next() on average, since we only 
    advance through the vectors when necessary.
Space Complexity: O(k) ~ O(1) for k vectors, since we store at most one element from
    each vector in the queue at any time.
"""
