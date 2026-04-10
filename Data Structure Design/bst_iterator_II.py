# Binary Search Tree Iterator II

"""
Implement the BSTIterator class that represents an iterator over the in-order traversal of a binary search tree (BST):

BSTIterator(TreeNode root) Initializes an object of the BSTIterator class. The root of the BST is given as part of the constructor. The pointer should be initialized to a non-existent number smaller than any element in the BST.
boolean hasNext() Returns true if there exists a number in the traversal to the right of the pointer, otherwise returns false.
int next() Moves the pointer to the right, then returns the number at the pointer.
boolean hasPrev() Returns true if there exists a number in the traversal to the left of the pointer, otherwise returns false.
int prev() Moves the pointer to the left, then returns the number at the pointer.
Notice that by initializing the pointer to a non-existent smallest number, the first call to next() will return the smallest element in the BST.

You may assume that next() and prev() calls will always be valid. That is, there will be at least a next/previous number in the in-order traversal when next()/prev() is called.

 

Example 1:



Input
["BSTIterator", "next", "next", "prev", "next", "hasNext", "next", "next", "next", "hasNext", "hasPrev", "prev", "prev"]
[[[7, 3, 15, null, null, 9, 20]], [null], [null], [null], [null], [null], [null], [null], [null], [null], [null], [null], [null]]
Output
[null, 3, 7, 3, 7, true, 9, 15, 20, false, true, 15, 9]

Explanation
// The underlined element is where the pointer currently is.
BSTIterator bSTIterator = new BSTIterator([7, 3, 15, null, null, 9, 20]); // state is   [3, 7, 9, 15, 20]
bSTIterator.next(); // state becomes [3, 7, 9, 15, 20], return 3
bSTIterator.next(); // state becomes [3, 7, 9, 15, 20], return 7
bSTIterator.prev(); // state becomes [3, 7, 9, 15, 20], return 3
bSTIterator.next(); // state becomes [3, 7, 9, 15, 20], return 7
bSTIterator.hasNext(); // return true
bSTIterator.next(); // state becomes [3, 7, 9, 15, 20], return 9
bSTIterator.next(); // state becomes [3, 7, 9, 15, 20], return 15
bSTIterator.next(); // state becomes [3, 7, 9, 15, 20], return 20
bSTIterator.hasNext(); // return false
bSTIterator.hasPrev(); // return true
bSTIterator.prev(); // state becomes [3, 7, 9, 15, 20], return 15
bSTIterator.prev(); // state becomes [3, 7, 9, 15, 20], return 9
 

Constraints:

The number of nodes in the tree is in the range [1, 105].
0 <= Node.val <= 106
At most 105 calls will be made to hasNext, next, hasPrev, and prev.
 

Follow up: Could you solve the problem without precalculating the values of the tree?
"""

# Definition for a binary tree node.
from pyparsing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BSTIterator:

    def __init__(self, root: TreeNode | None):
        self.stack = []
        self.history = []
        self.idx = -1  # pointer starts before the first element
        self._push_left(root)

    def _push_left(self, node: TreeNode | None) -> None:
        while node:
            self.stack.append(node)
            node = node.left

    def has_next(self) -> bool:
        return self.idx + 1 < len(self.history) or len(self.stack) > 0

    def next(self) -> int:
        self.idx += 1

        # already generated before
        if self.idx < len(self.history):
            return self.history[self.idx]

        # generate next inorder value lazily
        node = self.stack.pop()
        self.history.append(node.val)
        self._push_left(node.right)

        return node.val

    def has_prev(self) -> bool:
        return self.idx > 0

    def prev(self) -> int:
        self.idx -= 1
        return self.history[self.idx]
    
# Complexity Analysis
"""
Time Complexity: O(1) for has_next, has_prev, next, and prev. Each node is processed at most once in next(), and prev() just moves a pointer.
Space Complexity: O(h + k) where h is the height of the tree and k is the number of calls to next() (the size of history). In the worst case, h can be O(n) for a skewed tree, and k can be O(n) if we call next() for all nodes, leading to O(n) space in total.
"""

# Alternative Solution - Full inorder precompute version

class BSTIterator:

    def __init__(self, root: TreeNode | None):
        self.arr = []
        self.idx = -1
        self._inorder(root)

    def _inorder(self, node: TreeNode | None) -> None:
        if not node:
            return
        self._inorder(node.left)
        self.arr.append(node.val)
        self._inorder(node.right)

    def has_next(self) -> bool:
        return self.idx + 1 < len(self.arr)

    def next(self) -> int:
        self.idx += 1
        return self.arr[self.idx]

    def has_prev(self) -> bool:
        return self.idx > 0

    def prev(self) -> int:
        self.idx -= 1
        return self.arr[self.idx]
    
# Complexity Analysis
"""
Time Complexity: O(n) for the constructor due to the full inorder traversal. O(1) for has_next, next, has_prev, and prev.
Space Complexity: O(n) for storing the inorder traversal in arr.
"""
