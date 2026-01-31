# Data Stream as Disjoint Intervals

# Given a data stream input of non-negative integers a1, a2, ..., an, 
# summarize the numbers seen so far as a list of disjoint intervals.

from bisect import bisect_right

class SummaryRanges:
    def __init__(self):
        # intervals stored as parallel arrays
        self.starts = []
        self.ends = []

    def add_num(self, value: int) -> None:
        s, e = self.starts, self.ends
        n = len(s)
        if n == 0:
            s.append(value)
            e.append(value)
            return

        # i = first start > value, so left interval index is i-1, right is i
        i = bisect_right(s, value)

        # 1) check if value is already covered by left interval
        if i > 0 and e[i - 1] >= value:
            return

        # can we merge/extend with left?
        merge_left = (i > 0 and e[i - 1] + 1 == value)

        # can we merge/extend with right?
        merge_right = (i < n and s[i] - 1 == value)

        if merge_left and merge_right:
            # 2) bridge left and right: [s[i-1], e[i-1]] + value + [s[i], e[i]]
            e[i - 1] = e[i]          # extend left end to right end
            del s[i]                 # remove right interval
            del e[i]
        elif merge_left:
            # 3) extend left end
            e[i - 1] = value
        elif merge_right:
            # 4) extend right by shifting its start to value
            s[i] = value
        else:
            # 5) new interval [value, value]
            s.insert(i, value)
            e.insert(i, value)

    def get_intervals(self) -> list[list[int]]:
        return [[self.starts[i], self.ends[i]] for i in range(len(self.starts))]

# Complexities:
"""
Let m = number of disjoint intervals

1. addNum(value): O(m) -> Worst case
2. getIntervals(): O(m)

Space: O(m)
"""