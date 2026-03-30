# Two Sum - Data structure design

"""
Design a data structure that accepts a stream of integers and checks if it has a pair of integers that sum up to a particular value.

Implement the TwoSum class:

TwoSum() Initializes the TwoSum object, with an empty array initially.
void add(int number) Adds number to the data structure.
boolean find(int value) Returns true if there exists any pair of numbers whose sum is equal to value, otherwise, it returns false.
 

Example 1:

Input
["TwoSum", "add", "add", "add", "find", "find"]
[[], [1], [3], [5], [4], [7]]
Output
[null, null, null, null, true, false]

Explanation
TwoSum twoSum = new TwoSum();
twoSum.add(1);   // [] --> [1]
twoSum.add(3);   // [1] --> [1,3]
twoSum.add(5);   // [1,3] --> [1,3,5]
twoSum.find(4);  // 1 + 3 = 4, return true
twoSum.find(7);  // No two integers sum up to 7, return false
 

Constraints:

-105 <= number <= 105
-231 <= value <= 231 - 1
At most 104 calls will be made to add and find.
"""

# Idea
"""
Store numbers in a hash map (dictionary):

1. Key → number
2. Value → frequency (count)

This allows efficient lookup for complements.
"""

class TwoSum:

    def __init__(self):
        self.count = {}  # number -> frequency

    def add(self, number: int) -> None:
        if number in self.count:
            self.count[number] += 1
        else:
            self.count[number] = 1

    def find(self, value: int) -> bool:
        for num in self.count:
            complement = value - num

            if complement == num:
                # Need at least two occurrences
                if self.count[num] > 1:
                    return True
            else:
                if complement in self.count:
                    return True

        return False
    
# Complexity Analysis
"""
Time Complexity:
- add: O(1) - constant time to update the hash map.
- find: O(n) - where n is the number of unique numbers in the hash map.
Space Complexity:
- O(n) - where n is the number of unique numbers added to the hash map.
- O(1) - if we consider the range of numbers is limited and can be treated as constant.
"""
