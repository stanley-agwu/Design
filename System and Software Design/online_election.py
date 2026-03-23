# Online Election

"""
You are given two integer arrays persons and times. In an election, the ith 
vote was cast for persons[i] at time times[i].

For each query at a time t, find the person that was leading the election at 
time t. Votes cast at time t will count towards our query. In the case of a 
tie, the most recent vote (among tied candidates) wins.

Implement the TopVotedCandidate class:

TopVotedCandidate(int[] persons, int[] times) Initializes the object with 
    the persons and times arrays.
int q(int t) Returns the number of the person that was leading the election 
    at time t according to the mentioned rules.
 
Example 1:

Input
["TopVotedCandidate", "q", "q", "q", "q", "q", "q"]
[[[0, 1, 1, 0, 0, 1, 0], [0, 5, 10, 15, 20, 25, 30]], [3], [12], [25], [15], [24], [8]]
Output
[null, 0, 1, 1, 0, 0, 1]

Explanation
TopVotedCandidate topVotedCandidate = new TopVotedCandidate([0, 1, 1, 0, 0, 1, 0], 
    [0, 5, 10, 15, 20, 25, 30]);
topVotedCandidate.q(3); // return 0, At time 3, the votes are [0], and 0 is leading.
topVotedCandidate.q(12); // return 1, At time 12, the votes are [0,1,1], and 1 is leading.
topVotedCandidate.q(25); // return 1, At time 25, the votes are [0,1,1,0,0,1], 
    and 1 is leading (as ties go to the most recent vote.)
topVotedCandidate.q(15); // return 0
topVotedCandidate.q(24); // return 0
topVotedCandidate.q(8); // return 1

Constraints:

1 <= persons.length <= 5000
times.length == persons.length
0 <= persons[i] < persons.length
0 <= times[i] <= 109
times is sorted in a strictly increasing order.
times[0] <= t <= 109
At most 104 calls will be made to q.
"""

# Idea -> preprocessing plus binary search
"""
For every vote time times[i], precompute who is leading after that vote.

Then for a query q(t):
-> find the last index i such that times[i] <= t
-> return the precomputed leader at index i

This works because times is strictly increasing.

Important tie rule

When two candidates have the same number of votes, the most recent vote wins.

So while processing vote persons[i]:
-> increment that person's count
-> if their new count is greater than or equal to the current leader's count, make them the new leader

The >= is crucial. It handles ties by favoring the latest vote.
"""

from bisect import bisect_right
from typing import List


class TopVotedCandidate:

    def __init__(self, persons: List[int], times: List[int]):
        self.times = times
        self.leaders = []

        count = {}
        leader = -1
        leader_votes = 0

        for p in persons:
            count[p] = count.get(p, 0) + 1

            # >= is important: ties go to the most recent vote
            if count[p] >= leader_votes:
                leader = p
                leader_votes = count[p]

            self.leaders.append(leader)

    def q(self, t: int) -> int:
        # index of last time <= t
        idx = bisect_right(self.times, t) - 1
        return self.leaders[idx]
    
# Complexity Analysis:
# Initialization: O(n)
# Each query: O(log n) via binary search
# Space: O(n)

# With n <= 5000 and at most 10^4 queries, this is easily efficient enough.