# Serialize and Deserialize a Binary Search Tree (BST)

"""
Serialization is converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary search tree. There is no restriction on how your serialization/deserialization algorithm should work. You need to ensure that a binary search tree can be serialized to a string, and this string can be deserialized to the original tree structure.

The encoded string should be as compact as possible.

 

Example 1:

Input: root = [2,1,3]
Output: [2,1,3]
Example 2:

Input: root = []
Output: []
 

Constraints:

The number of nodes in the tree is in the range [0, 104].
0 <= Node.val <= 104
The input tree is guaranteed to be a binary search tree.
"""

# Idea -> Use the BST property.
"""
A compact approach is:

-> Serialize with preorder traversal: root, left, right
-> Do not store null markers
-> Deserialize by rebuilding from preorder using value bounds
    for a BST, every node in the left subtree must be in (low, root.val)
    every node in the right subtree must be in (root.val, high)

This gives a compact encoding and linear reconstruction.
"""

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Codec:
    def serialize(self, root):
        vals = []

        def preorder(node):
            if not node:
                return
            vals.append(str(node.val))
            preorder(node.left)
            preorder(node.right)

        preorder(root)
        return ",".join(vals)

    def deserialize(self, data):
        if not data:
            return None

        preorder = list(map(int, data.split(",")))
        self.i = 0

        def build(low, high):
            if self.i == len(preorder):
                return None

            val = preorder[self.i]
            if val < low or val > high:
                return None

            self.i += 1
            node = TreeNode(val)
            node.left = build(low, val)
            node.right = build(val, high)
            return node

        return build(float("-inf"), float("inf"))
    
# Complexity analysis
"""
Let n be the number of nodes.

Serialize
Time: O(n)
Space: O(n) for the output string, plus recursion stack O(h) where h is tree height

Deserialize
Time: O(n) each value is processed once
Space: O(n) for the parsed preorder list, plus recursion stack O(h)
"""
