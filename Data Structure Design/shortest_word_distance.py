# Shortest Word Distance

"""
Design a data structure that will be initialized with a string array, and then 
it should answer queries of the shortest distance between two different strings 
from the array.

Implement the WordDistance class:

WordDistance(String[] wordsDict) initializes the object with the strings array 
    wordsDict.
int shortest(String word1, String word2) returns the shortest distance between 
    word1 and word2 in the array wordsDict.

Example 1:

Input
["WordDistance", "shortest", "shortest"]
[[["practice", "makes", "perfect", "coding", "makes"]], ["coding", "practice"], 
["makes", "coding"]]

Output
[null, 3, 1]

Explanation
WordDistance wordDistance = new WordDistance(["practice", "makes", "perfect", 
    "coding", "makes"]);
wordDistance.shortest("coding", "practice"); // return 3
wordDistance.shortest("makes", "coding");    // return 1

Constraints:

1 <= wordsDict.length <= 3 * 104
1 <= wordsDict[i].length <= 10
wordsDict[i] consists of lowercase English letters.
word1 and word2 are in wordsDict.
word1 != word2
At most 5000 calls will be made to shortest.
"""

from collections import defaultdict
from typing import List

class WordDistance:

    def __init__(self, words_dict: List[str]):
        self.positions = defaultdict(list)

        for i, word in enumerate(words_dict):
            self.positions[word].append(i)

    def shortest(self, word1: str, word2: str) -> int:
        pos1 = self.positions[word1]
        pos2 = self.positions[word2]

        i = 0
        j = 0
        result = float("inf")

        while i < len(pos1) and j < len(pos2):
            result = min(result, abs(pos1[i] - pos2[j]))

            if pos1[i] < pos2[j]:
                i += 1
            else:
                j += 1

        return result

# Complexity Analysis
"""
Let n be the length of wordsDict and m be the number of calls to shortest.
Initialization:
Time Complexity: O(n) to build the positions dictionary.
Space Complexity: O(n) for storing the positions of each word.
shortest method:
Time Complexity: O(p + q) where p and q are the number of occurrences 
    of word1 and word2 respectively. In the worst case, this can be 
    O(n) if both words appear frequently.
Space Complexity: O(1) for the pointers and result variable.
Overall, the initialization is O(n) time and space, and each call to 
shortest is O(p + q) time and O(1) space.
"""