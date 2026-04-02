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
A Segment Tree is a good fit here because it supports both operations efficiently:
1. update(index, val) in O(log n)
2. sumRange(left, right) in O(log n)

This is much better than recomputing sums each time.
Each node in the segment tree stores the sum of a subarray.

For example, for nums = [1, 3, 5]:

root stores sum of [0..2] = 9
left child stores sum of [0..1] = 4
right child stores sum of [2..2] = 5

When we update one element, we only update the nodes along that path from leaf to root.
When we query a range sum, we only visit the nodes that overlap with that range.
"""

class NumArray:
    def __init__(self, nums: list[int]):
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)
        self.nums = nums[:]

        def build(node: int, start: int, end: int) -> None:
            if start == end:
                self.tree[node] = nums[start]
                return

            mid = (start + end) // 2
            left_child = 2 * node
            right_child = 2 * node + 1

            build(left_child, start, mid)
            build(right_child, mid + 1, end)

            self.tree[node] = self.tree[left_child] + self.tree[right_child]

        build(1, 0, self.n - 1)

    def update(self, index: int, val: int) -> None:
        def update_tree(node: int, start: int, end: int) -> None:
            if start == end:
                self.tree[node] = val
                self.nums[index] = val
                return

            mid = (start + end) // 2
            left_child = 2 * node
            right_child = 2 * node + 1

            if index <= mid:
                update_tree(left_child, start, mid)
            else:
                update_tree(right_child, mid + 1, end)

            self.tree[node] = self.tree[left_child] + self.tree[right_child]

        update_tree(1, 0, self.n - 1)

    def sum_range(self, left: int, right: int) -> int:
        def query(node: int, start: int, end: int, left: int, right: int) -> int:
            # completely outside
            if right < start or end < left:
                return 0

            # completely inside
            if left <= start and end <= right:
                return self.tree[node]

            mid = (start + end) // 2
            left_sum = query(2 * node, start, mid, left, right)
            right_sum = query(2 * node + 1, mid + 1, end, left, right)

            return left_sum + right_sum

        return query(1, 0, self.n - 1, left, right)


# Complexity Analysis
# - Time complexity: O(log n) for each update and sumRange query, O(n) for initialization
# - Space complexity: O(n) for storing the segment tree and the input array
# - Total time complexity: O(n + q log n) where n is the length of the input array and q is the number of queries
# - Total space complexity: O(n) for storing the segment tree and the input array

"""
__init__: O(n)
update: O(log n)
sum_range: O(log n)
Space
Segment tree: O(n)
"""