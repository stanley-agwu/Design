# Design Linked List

"""
Design your implementation of the linked list. You can choose to use a 
singly or doubly linked list. A node in a singly linked list should have 
two attributes: val and next. val is the value of the current node, and 
next is a pointer/reference to the next node.

If you want to use the doubly linked list, you will need one more 
attribute prev to indicate the previous node in the linked list. 
Assume all nodes in the linked list are 0-indexed.

Implement the MyLinkedList class:

MyLinkedList() Initializes the MyLinkedList object.
int get(int index) Get the value of the indexth node in the linked list. 
    If the index is invalid, return -1.
void addAtHead(int val) Add a node of value val before the first element of 
    the linked list. After the insertion, the new node will be the first node
    of the linked list.
void addAtTail(int val) Append a node of value val as the last element of 
    the linked list.
void addAtIndex(int index, int val) Add a node of value val before the 
    indexth node in the linked list. If index equals the length of the linked
    list, the node will be appended to the end of the linked list. If index 
    is greater than the length, the node will not be inserted.
void deleteAtIndex(int index) Delete the indexth node in the linked list, 
    if the index is valid.
 

Example 1:

Input
["MyLinkedList", "addAtHead", "addAtTail", "addAtIndex", "get", "deleteAtIndex", "get"]
[[], [1], [3], [1, 2], [1], [1], [1]]
Output
[null, null, null, null, 2, null, 3]

Explanation
MyLinkedList myLinkedList = new MyLinkedList();
myLinkedList.addAtHead(1);
myLinkedList.addAtTail(3);
myLinkedList.addAtIndex(1, 2);    // linked list becomes 1->2->3
myLinkedList.get(1);              // return 2
myLinkedList.deleteAtIndex(1);    // now the linked list is 1->3
myLinkedList.get(1);              // return 3
"""

class Node:
    def __init__(self, val=0):
        self.val = val
        self.prev = None
        self.next = None


class MyLinkedList:

    def __init__(self):
        self.size = 0

        # Sentinel nodes
        self.head = Node(0)
        self.tail = Node(0)

        self.head.next = self.tail
        self.tail.prev = self.head

    def _get_node(self, index: int) -> Node:
        """
        Return the node at 0-based index.
        Assumes index is valid.
        """
        if index < self.size // 2:
            curr = self.head.next
            for _ in range(index):
                curr = curr.next
        else:
            curr = self.tail.prev
            for _ in range(self.size - 1, index, -1):
                curr = curr.prev
        return curr

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1
        return self._get_node(index).val

    def add_at_head(self, val: int) -> None:
        self.addAtIndex(0, val)

    def add_at_tail(self, val: int) -> None:
        self.addAtIndex(self.size, val)

    def add_at_index(self, index: int, val: int) -> None:
        if index < 0:
            index = 0
        if index > self.size:
            return

        # Find node that will be AFTER the new node
        if index == self.size:
            succ = self.tail
            pred = self.tail.prev
        else:
            succ = self._get_node(index)
            pred = succ.prev

        new_node = Node(val)
        new_node.prev = pred
        new_node.next = succ
        pred.next = new_node
        succ.prev = new_node

        self.size += 1

    def delete_at_index(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return

        node = self._get_node(index)
        pred = node.prev
        succ = node.next

        pred.next = succ
        succ.prev = pred

        self.size -= 1
