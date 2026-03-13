# Binary Search Tree Traversals

"""
|--------------------------------------------------------------|
| Traversal         | Order               | Use                |
| ----------------- | ------------------- | ------------------ |
| Pre-order (DFS)   | Node → Left → Right | Copy tree          |
| In-order          | Left → Node → Right | Sorted order (BST) |
| Post-order        | Left → Right → Node | Delete tree        |
| Level-order       | BFS                 | shortest path      |
|--------------------------------------------------------------|
"""

class TreeNode:
    __slot__ = ("val", "left", "right")
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# 1. In-order Traversal

# Left → Node → Right
# NOTE: In-order Traversals present node values in sorted order (increasing order)

# Recursive in-order traversal
def inorder(root: TreeNode | None):
    if not root:
        return

    inorder(root.left)
    print(root.val)
    inorder(root.right)

# Iterative in-order traversal (using stack)
def inorder(root: TreeNode | None):
    stack = []
    node = root

    while stack or node:
        while node:
            stack.append(node)
            node = node.left

        node = stack.pop()
        print(node.val)

        node = node.right


# 2. Pre-order Traversal (Depth-First Search Traversal)

# Node → Left → Right
# NOTE: Level order uses stack, not queue.
"""
Pre-order is used for:
Copy tree, Serialize tree, Build tree, DFS problems
"""

# Recursive Pre-order traversal
def preorder(root):
    if not root:
        return

    print(root.val)
    preorder(root.left)
    preorder(root.right)


# Iterative Pre-order traversal
def preorder(root):
    if not root:
        return []

    stack = [root]
    result = []

    while stack:
        node = stack.pop()

        result.append(node.val)

        if node.right: # This comes first
            stack.append(node.right)

        if node.left: # This comes second/next
            stack.append(node.left)

    return result


# 3. Post-order Traversal

# Left → Right → Node

# Recursive Post-order traversal
def postorder(root):
    if not root:
        return

    postorder(root.left)
    postorder(root.right)
    print(root.val)


# Iterative Post-order traversal
def postorder(root):
    if not root:
        return []

    stack = [root]
    result = []

    while stack:
        node = stack.pop()

        result.append(node.val)

        if node.left:
            stack.append(node.left)

        if node.right:
            stack.append(node.right)

    return result[::-1]


# 4. Level-order Traversal (Breadth-First search Traversal)

# Level 0 → Level 1 → Level 2 → ...
# NOTE: Level order uses queue, not stack. Queue = FIFO.

# Level-order traversal (Breadth-First search Traversal)
# NOTE: Only Iterative Approach

from collections import deque

def level_order(root):
    if not root:
        return []

    queue = deque([root])
    result = []

    while queue:
        node = queue.popleft()

        result.append(node.val)

        if node.left:
            queue.append(node.left)

        if node.right:
            queue.append(node.right)

    return result
