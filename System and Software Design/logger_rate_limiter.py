# Logger Rate Limiter

"""
Design a logger system that receives a stream of messages along with their 
timestamps. Each unique message should only be printed at most every 10 
seconds (i.e. a message printed at timestamp t will prevent other identical 
messages from being printed until timestamp t + 10).

All messages will come in chronological order. Several messages may arrive 
at the same timestamp.

Implement the Logger class:

Logger() Initializes the logger object.
bool shouldPrintMessage(int timestamp, string message) Returns true if the 
message should be printed in the given timestamp, otherwise returns false.
 
Example 1:

Input
["Logger", "shouldPrintMessage", "shouldPrintMessage", "shouldPrintMessage", "shouldPrintMessage", "shouldPrintMessage", "shouldPrintMessage"]
[[], [1, "foo"], [2, "bar"], [3, "foo"], [8, "bar"], [10, "foo"], [11, "foo"]]
Output
[null, true, true, false, false, false, true]

Explanation
Logger logger = new Logger();
logger.shouldPrintMessage(1, "foo");  // return true, next allowed timestamp 
    for "foo" is 1 + 10 = 11
logger.shouldPrintMessage(2, "bar");  // return true, next allowed timestamp 
    for "bar" is 2 + 10 = 12
logger.shouldPrintMessage(3, "foo");  // 3 < 11, return false
logger.shouldPrintMessage(8, "bar");  // 8 < 12, return false
logger.shouldPrintMessage(10, "foo"); // 10 < 11, return false
logger.shouldPrintMessage(11, "foo"); // 11 >= 11, return true, next allowed 
timestamp for "foo" is 11 + 10 = 21
 
Constraints:

0 <= timestamp <= 109
Every timestamp will be passed in non-decreasing order (chronological order).
1 <= message.length <= 30
At most 104 calls will be made to shouldPrintMessage.
"""

# Idea
"""
This is a classic rate-limiting design problem. 
For each message, you only need to remember:

When was the last time this message was printed?

Then:

If current_timestamp >= last_printed + 10 → allow
Else → reject
"""

class Logger:

    def __init__(self):
        self.last_print = {}

    def should_print_message(self, timestamp: int, message: str) -> bool:
        if message not in self.last_print:
            self.last_print[message] = timestamp
            return True

        if timestamp >= self.last_print[message] + 10:
            self.last_print[message] = timestamp
            return True

        return False
    
# Time complexity: O(1) for each call to should_print_message
# Space complexity: O(M) where M is the number of unique messages that have been printed at least once.

# Alternative Solution

from collections import deque

class Logger:

    def __init__(self):
        self.queue = deque()
        self.active = set()

    def should_print_message(self, timestamp: int, message: str) -> bool:
        # Remove expired messages
        while self.queue and self.queue[0][0] <= timestamp - 10:
            old_time, old_msg = self.queue.popleft()
            self.active.remove(old_msg)

        if message in self.active:
            return False

        self.queue.append((timestamp, message))
        self.active.add(message)
        return True

# Time complexity: O(1) amortized for each call to should_print_message, since each message is added and removed from the queue at most once.
# Space complexity: O(M) where M is the number of unique messages that have been printed in the last 10 seconds.
