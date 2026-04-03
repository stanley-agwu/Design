# Design Hit Counter

"""
Design a hit counter which counts the number of hits received in the past 5 
minutes (i.e., the past 300 seconds).

Your system should accept a timestamp parameter (in seconds granularity), 
and you may assume that calls are being made to the system in chronological 
order (i.e., timestamp is monotonically increasing). Several hits may arrive 
roughly at the same time.

Implement the HitCounter class:

HitCounter() Initializes the object of the hit counter system.
void hit(int timestamp) Records a hit that happened at timestamp (in seconds). 
    Several hits may happen at the same timestamp.
int getHits(int timestamp) Returns the number of hits in the past 5 minutes 
    from timestamp (i.e., the past 300 seconds).
 
Example 1:

Input
["HitCounter", "hit", "hit", "hit", "getHits", "hit", "getHits", "getHits"]
[[], [1], [2], [3], [4], [300], [300], [301]]
Output
[null, null, null, null, 3, null, 4, 3]

Explanation
HitCounter hitCounter = new HitCounter();
hitCounter.hit(1);       // hit at timestamp 1.
hitCounter.hit(2);       // hit at timestamp 2.
hitCounter.hit(3);       // hit at timestamp 3.
hitCounter.getHits(4);   // get hits at timestamp 4, return 3.
hitCounter.hit(300);     // hit at timestamp 300.
hitCounter.getHits(300); // get hits at timestamp 300, return 4.
hitCounter.getHits(301); // get hits at timestamp 301, return 3.
 
Constraints:

1 <= timestamp <= 2 * 109
All the calls are being made to the system in chronological order 
(i.e., timestamp is monotonically increasing).
At most 300 calls will be made to hit and getHits.
 
Follow up: What if the number of hits per second could be huge? Does your design scale?
"""

# Idea
"""
Use a queue of (timestamp, count) pairs and keep a running total of hits in 
the last 300 seconds.

Because timestamps are non-decreasing, expired hits are always at the front, 
so cleanup is efficient.
"""

from collections import deque


class HitCounter:

    def __init__(self):
        self.q = deque()          # (timestamp, count)
        self.total = 0

    def _remove_expired(self, timestamp: int) -> None:
        # Keep only hits in the last 300 seconds: [timestamp - 299, timestamp]
        while self.q and self.q[0][0] <= timestamp - 300:
            old_time, old_count = self.q.popleft()
            self.total -= old_count

    def hit(self, timestamp: int) -> None:
        self._remove_expired(timestamp)

        if self.q and self.q[-1][0] == timestamp:
            t, cnt = self.q[-1]
            self.q[-1] = (t, cnt + 1)
        else:
            self.q.append((timestamp, 1))

        self.total += 1

    def get_hits(self, timestamp: int) -> int:
        self._remove_expired(timestamp)
        return self.total
    
# Time complexity: O(1) for hit() and O(k) for get_hits() where k is the number of expired hits removed.
# Space complexity: O(n) where n is the number of hits in the last 300 seconds.
