# Range Module

"""
A Range Module is a module that tracks ranges of numbers. Design a 
data structure to track the ranges represented as half-open intervals 
and query about them.

A half-open interval [left, right) denotes all the real numbers x 
where left <= x < right.

Implement the RangeModule class:

RangeModule() Initializes the object of the data structure.
void addRange(int left, int right) Adds the half-open interval [left, right), 
    tracking every real number in that interval. Adding an interval 
    that partially overlaps with currently tracked numbers should add 
    any numbers in the interval [left, right) that are not already 
    tracked.
boolean queryRange(int left, int right) Returns true if every real 
    number in the interval [left, right) is currently being tracked, 
    and false otherwise.
void removeRange(int left, int right) Stops tracking every real number 
    currently being tracked in the half-open interval [left, right).
 

Example 1:

Input
["RangeModule", "addRange", "removeRange", "queryRange", "queryRange", "queryRange"]
[[], [10, 20], [14, 16], [10, 14], [13, 15], [16, 17]]
Output
[null, null, null, true, false, true]

Explanation
RangeModule rangeModule = new RangeModule();
rangeModule.addRange(10, 20);
rangeModule.removeRange(14, 16);
rangeModule.queryRange(10, 14); // return True,(Every number in [10, 14) is being tracked)
rangeModule.queryRange(13, 15); // return False,(Numbers like 14, 14.03, 14.17 in [13, 15) are not being tracked)
rangeModule.queryRange(16, 17); // return True, (The number 16 in [16, 17) is still being tracked, despite the remove operation)
 

Constraints:

1 <= left < right <= 109
At most 104 calls will be made to addRange, queryRange, and removeRange.
"""

from bisect import bisect_left, bisect_right

class RangeModule:
    def __init__(self):
        # stores disjoint, sorted intervals [start, end)
        self.intervals = []

    def add_range(self, left: int, right: int) -> None:
        intervals = self.intervals
        n = len(intervals)

        # Find where to start merging
        i = bisect_left(intervals, [left, -float('inf')])

        # If previous interval touches/overlaps, include it
        if i > 0 and intervals[i - 1][1] >= left:
            i -= 1

        new_left, new_right = left, right
        j = i

        # Merge all overlapping/touching intervals
        while j < n and intervals[j][0] <= new_right:
            new_left = min(new_left, intervals[j][0])
            new_right = max(new_right, intervals[j][1])
            j += 1

        intervals[i:j] = [[new_left, new_right]]

    def query_range(self, left: int, right: int) -> bool:
        intervals = self.intervals

        # Find the interval with largest start <= left
        i = bisect_right(intervals, [left, float('inf')]) - 1

        return i >= 0 and intervals[i][0] <= left and intervals[i][1] >= right

    def remove_range(self, left: int, right: int) -> None:
        intervals = self.intervals
        n = len(intervals)

        # Find first possibly overlapping interval
        i = bisect_left(intervals, [left, -float('inf')])

        if i > 0 and intervals[i - 1][1] > left:
            i -= 1

        new_parts = []
        j = i

        while j < n and intervals[j][0] < right:
            start, end = intervals[j]

            # Left piece remains
            if start < left:
                new_parts.append([start, left])

            # Right piece remains
            if end > right:
                new_parts.append([right, end])

            j += 1

        intervals[i:j] = new_parts

# Time complexity
# Let n be the number of stored disjoint intervals.
# addRange: O(log n + k)
# queryRange: O(log n)
# removeRange: O(log n + k)

# O(n) - Space complexity