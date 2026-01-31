# Stream of Characters

# Design an algorithm that accepts a stream of characters and checks if a 
# suffix of these characters is a string of a given array of strings words.

# For example, if words = ["abc", "xyz"] and the stream added the four characters 
# (one by one) 'a', 'x', 'y', and 'z', your algorithm should detect that the suffix 
# "xyz" of the characters "axyz" matches "xyz" from words.

from collections import deque

class TrieNode:
    __slots__ = ("children", "is_end")
    def __init__(self):
        self.children = {}      # char -> TrieNode
        self.is_end = False

class StreamChecker:
    def __init__(self, words: list[str]):
        self.root = TrieNode()
        self.max_len = 0

        for word in words:
            self.max_len = max(self.max_len, len(word))
            node = self.root
            for char in reversed(word):
                next_node = node.children.get(char)
                if next_node is None:
                    next_node = TrieNode()
                    node.children[char] = next_node
                node = next_node
            node.is_end = True

        self.stream = deque()  # store latest chars, newest at right

    def query(self, letter: str) -> bool:
        self.stream.append(letter)
        if len(self.stream) > self.max_len:
            self.stream.popleft()

        node = self.root
        # traverse from newest to oldest
        for char in reversed(self.stream):
            node = node.children.get(char)
            if node is None:
                return False
            if node.is_end:
                return True
        return False

# Complexities:
"""
Let L = max(len(word)), N = len(words)

1. Build trie: O(total characters in words) => L * N
2. Each query: O(L) worst-case (≤ L)

Memory: O(total characters in words) => L * N
"""