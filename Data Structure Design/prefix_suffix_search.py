# Prefix and Suffix Search

"""
Design a special dictionary that searches the words in it by a prefix and a suffix.

Implement the WordFilter class:

WordFilter(string[] words) Initializes the object with the words in the dictionary.
f(string pref, string suff) Returns the index of the word in the dictionary, 
which has the prefix pref and the suffix suff. If there is more than one 
valid index, return the largest of them. If there is no such word in the 
dictionary, return -1.
 
Example 1:

Input
["WordFilter", "f"]
[[["apple"]], ["a", "e"]]
Output
[null, 0]
Explanation
WordFilter wordFilter = new WordFilter(["apple"]);
wordFilter.f("a", "e"); // return 0, because the word at index 0 has 
prefix = "a" and suffix = "e".
 
Constraints:

1 <= words.length <= 104
1 <= words[i].length <= 7
1 <= pref.length, suff.length <= 7
words[i], pref and suff consist of lowercase English letters only.
At most 104 calls will be made to the function f.
"""

# Idea -> precomputation of all prefix + suffix combinations for every word
"""
Because each word is very short (length <= 7), the most efficient practical 
solution is to precompute all prefix + suffix combinations for every word 
and store the largest index for each pair.

That gives:

-> Construction: O(n * L^2) where L <= 7
-> Query: O(1)
This is ideal since there can be up to 10^4 queries.
"""

class WordFilter:
    def __init__(self, words: list[str]):
        self.lookup = {}

        for i, word in enumerate(words):
            n = len(word)

            for p_len in range(1, n + 1):
                pref = word[:p_len]
                for s_start in range(n):
                    suff = word[s_start:]
                    self.lookup[(pref, suff)] = i

    def f(self, pref: str, suff: str) -> int:
        return self.lookup.get((pref, suff), -1)


# Time complexity ≈ O(n + q)
# Space complexity ≈ O(n)