# Alien Dictionary

"""
There is a new alien language that uses the English alphabet. However, the order of the letters is unknown to you.

You are given a list of strings words from the alien language's dictionary. Now it is claimed that the strings in words are sorted lexicographically by the rules of this new language.

If this claim is incorrect, and the given arrangement of string in words cannot correspond to any order of letters, return "".

Otherwise, return a string of the unique letters in the new alien language sorted in lexicographically increasing order by the new language's rules. If there are multiple solutions, return any of them.

 

Example 1:

Input: words = ["wrt","wrf","er","ett","rftt"]
Output: "wertf"
Example 2:

Input: words = ["z","x"]
Output: "zx"
Example 3:

Input: words = ["z","x","z"]
Output: ""
Explanation: The order is invalid, so return "".
 

Constraints:

1 <= words.length <= 100
1 <= words[i].length <= 100
words[i] consists of only lowercase English letters.
"""

from collections import deque


def alien_order(words: list[str]) -> str:
    # Step 1: initialize graph with all unique characters
    graph = {ch: set() for word in words for ch in word}
    indegree = {ch: 0 for ch in graph}

    # Step 2: build edges from adjacent words
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))

        # Invalid case: prefix order is wrong
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""

        # Find first different character
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in graph[w1[j]]:
                    graph[w1[j]].add(w2[j])
                    indegree[w2[j]] += 1
                break

    # Step 3: topological sort (Kahn's algorithm)
    queue = deque([ch for ch in indegree if indegree[ch] == 0])
    order = []

    while queue:
        ch = queue.popleft()
        order.append(ch)

        for nei in graph[ch]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)

    # Step 4: detect cycle
    if len(order) != len(graph):
        return ""

    return "".join(order)
    
# Time complexity: O(C + N) where C is the total number of characters in all words and N is the number of unique characters.
# Space complexity: O(C + N) for the graph and indegree structures.

print(alien_order(["wrt","wrf","er","ett","rftt"]))  # Output: "wertf"
print(alien_order(["z","x"]))  # Output: "zx"
print(alien_order(["z","x","z"]))  # Output: ""



