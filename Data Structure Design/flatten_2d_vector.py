# Flatten 2D Vector

"""
Design an iterator to flatten a 2D vector. It should support the next and hasNext operations.

Implement the Vector2D class:

Vector2D(int[][] vec) initializes the object with the 2D vector vec.
next() returns the next element from the 2D vector and moves the pointer one step forward. You may assume that all the calls to next are valid.
hasNext() returns true if there are still some elements in the vector, and false otherwise.
 

Example 1:

Input
["Vector2D", "next", "next", "next", "hasNext", "hasNext", "next", "hasNext"]
[[[[1, 2], [3], [4]]], [], [], [], [], [], [], []]
Output
[null, 1, 2, 3, true, true, 4, false]

Explanation
Vector2D vector2D = new Vector2D([[1, 2], [3], [4]]);
vector2D.next();    // return 1
vector2D.next();    // return 2
vector2D.next();    // return 3
vector2D.hasNext(); // return True
vector2D.hasNext(); // return True
vector2D.next();    // return 4
vector2D.hasNext(); // return False
 

Constraints:

0 <= vec.length <= 200
0 <= vec[i].length <= 500
-500 <= vec[i][j] <= 500
At most 105 calls will be made to next and hasNext.
"""

from typing import List


class Vector2D:

    def __init__(self, vec: list[list[int]]):
        self.vec = vec
        self.row = 0
        self.col = 0
        self._advance_to_next()

    def _advance_to_next(self):
        # Move to next non-empty position
        while self.row < len(self.vec) and self.col >= len(self.vec[self.row]):
            self.row += 1
            self.col = 0

    def next(self) -> int:
        val = self.vec[self.row][self.col]
        self.col += 1
        self._advance_to_next()
        return val

    def has_next(self) -> bool:
        return self.row < len(self.vec)
    
# Complexity Analysis
"""
Time Complexity: O(1) for next() and has_next() on average, 
    since we only advance through the vector when necessary.
Space Complexity: O(1) for the iterator itself, but O(n) for storing 
    the input vector.
"""