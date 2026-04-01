# Moving Average from Data Stream

"""
Given a stream of integers and a window size, calculate the moving average of 
all integers in the sliding window.

Implement the MovingAverage class:

MovingAverage(int size) Initializes the object with the size of the window size.
double next(int val) Returns the moving average of the last size values of the stream.

Example 1:

Input
["MovingAverage", "next", "next", "next", "next"]
[[3], [1], [10], [3], [5]]
Output
[null, 1.0, 5.5, 4.66667, 6.0]

Explanation
MovingAverage movingAverage = new MovingAverage(3);
movingAverage.next(1); // return 1.0 = 1 / 1
movingAverage.next(10); // return 5.5 = (1 + 10) / 2
movingAverage.next(3); // return 4.66667 = (1 + 10 + 3) / 3
movingAverage.next(5); // return 6.0 = (10 + 3 + 5) / 3

Constraints:

1 <= size <= 1000
-105 <= val <= 105
At most 104 calls will be made to next.
"""

# Idea
"""
This is a classic sliding window problem. The key is to avoid recomputing the 
sum every time.

Maintain:

1. A queue (to keep last size elements)
2. A running sum of the current window.

So each operation is O(1).
"""

from collections import deque


class MovingAverage:

    def __init__(self, size: int):
        self.size = size
        self.queue = deque()
        self.window_sum = 0

    def next(self, val: int) -> float:
        # Add new value
        self.queue.append(val)
        self.window_sum += val

        # Remove oldest if window exceeds size
        if len(self.queue) > self.size:
            removed = self.queue.popleft()
            self.window_sum -= removed

        # Compute average
        return self.window_sum / len(self.queue)
    
# Complexity Analysis:
"""
Time Complexity: O(1) for each call to next.
Space Complexity: O(size) for the queue storing the last size elements.
"""
