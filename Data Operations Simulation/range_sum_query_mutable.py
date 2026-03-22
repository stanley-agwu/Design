# Range Sum Query - Mutable

"""
Given an integer array nums, handle multiple queries of the following types:

1. Update the value of an element in nums.
2. Calculate the sum of the elements of nums between indices left and right 
    inclusive where left <= right.
Implement the NumArray class:

- NumArray(int[] nums) Initializes the object with the integer array nums.
- void update(int index, int val) Updates the value of nums[index] to be val.
- int sumRange(int left, int right) Returns the sum of the elements of nums 
    between indices left and right inclusive (i.e. nums[left] + nums[left + 1] + ... + nums[right]).
 
Example 1:

Input
["NumArray", "sumRange", "update", "sumRange"]
[[[1, 3, 5]], [0, 2], [1, 2], [0, 2]]
Output
[null, 9, null, 8]

Explanation
NumArray numArray = new NumArray([1, 3, 5]);
numArray.sumRange(0, 2); // return 1 + 3 + 5 = 9
numArray.update(1, 2);   // nums = [1, 2, 5]
numArray.sumRange(0, 2); // return 1 + 2 + 5 = 8
 
Constraints:

1 <= nums.length <= 3 * 104
-100 <= nums[i] <= 100
0 <= index < nums.length
-100 <= val <= 100
0 <= left <= right < nums.length
At most 3 * 104 calls will be made to update and sumRange.
"""

# Idea:

"""
Use a Fenwick Tree (Binary Indexed Tree) or a Segment Tree.

For this problem, the cleanest solution is a Fenwick Tree because it supports:

-> update(index, val) in O(log n)
-> sumRange(left, right) in O(log n)
-> construction in O(n log n)

That is efficient enough for 3 * 10^4 operations.

Fenwick Tree intuition

A Fenwick Tree stores partial sums in a smart way so that:

-> updating one value only affects a few nodes
-> computing prefix sums also visits only a few nodes
Core operations
-> add(i, delta) → add delta to index i
-> prefixSum(i) → sum of elements from 0 to i

Then:
sumRange(left, right) = prefixSum(right) - prefixSum(left - 1)
"""

class NumArray:
    def __init__(self, nums: list[int]):
        self.n = len(nums)
        self.nums = nums[:]                  # keep current values
        self.bit = [0] * (self.n + 1)       # 1-based Fenwick Tree

        for i, val in enumerate(nums):
            self._add(i + 1, val)

    def _add(self, index: int, delta: int) -> None:
        while index <= self.n:
            self.bit[index] += delta
            index += index & -index

    def _prefix_sum(self, index: int) -> int:
        s = 0
        while index > 0:
            s += self.bit[index]
            index -= index & -index
        return s

    def update(self, index: int, val: int) -> None:
        delta = val - self.nums[index]
        self.nums[index] = val
        self._add(index + 1, delta)

    def sum_range(self, left: int, right: int) -> int:
        return self._prefix_sum(right + 1) - self._prefix_sum(left)
    
# Complexity Analysis
# - Time complexity: O(log n) for each update and sumRange query, 
#                       O(n log n) for initialization
# - Space complexity: O(n) for storing the Fenwick Tree and the current values