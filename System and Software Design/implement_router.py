# Implement Router

"""
Design a data structure that can efficiently manage data packets in a 
network router. Each data packet consists of the following attributes:

source: A unique identifier for the machine that generated the packet.
destination: A unique identifier for the target machine.
timestamp: The time at which the packet arrived at the router.
Implement the Router class:

Router(int memoryLimit): Initializes the Router object with a fixed memory limit.

memoryLimit is the maximum number of packets the router can store at any given time.
If adding a new packet would exceed this limit, the oldest packet must be 
removed to free up space.
bool addPacket(int source, int destination, int timestamp): Adds a packet 
    with the given attributes to the router.

A packet is considered a duplicate if another packet with the same source, 
destination, and timestamp already exists in the router.
Return true if the packet is successfully added (i.e., it is not a duplicate); 
otherwise return false.
int[] forwardPacket(): Forwards the next packet in FIFO (First In First Out) order.

Remove the packet from storage.
Return the packet as an array [source, destination, timestamp].
If there are no packets to forward, return an empty array.
int getCount(int destination, int startTime, int endTime):

Returns the number of packets currently stored in the router (i.e., not yet forwarded) 
that have the specified destination and have timestamps in the inclusive range [startTime, endTime].
Note that queries for addPacket will be made in non-decreasing order of timestamp.

 

Example 1:

Input:
["Router", "addPacket", "addPacket", "addPacket", "addPacket", "addPacket", 
    "forwardPacket", "addPacket", "getCount"]
[[3], [1, 4, 90], [2, 5, 90], [1, 4, 90], [3, 5, 95], [4, 5, 105], [], 
    [5, 2, 110], [5, 100, 110]]

Output:
[null, true, true, false, true, true, [2, 5, 90], true, 1]

Explanation

Router router = new Router(3); // Initialize Router with memoryLimit of 3.
router.addPacket(1, 4, 90); // Packet is added. Return True.
router.addPacket(2, 5, 90); // Packet is added. Return True.
router.addPacket(1, 4, 90); // This is a duplicate packet. Return False.
router.addPacket(3, 5, 95); // Packet is added. Return True
router.addPacket(4, 5, 105); // Packet is added, [1, 4, 90] is removed as 
    number of packets exceeds memoryLimit. Return True.
router.forwardPacket(); // Return [2, 5, 90] and remove it from router.
router.addPacket(5, 2, 110); // Packet is added. Return True.
router.getCount(5, 100, 110); // The only packet with destination 5 and 
    timestamp in the inclusive range [100, 110] is [4, 5, 105]. Return 1.
Example 2:

Input:
["Router", "addPacket", "forwardPacket", "forwardPacket"]
[[2], [7, 4, 90], [], []]

Output:
[null, true, [7, 4, 90], []]

Explanation

Router router = new Router(2); // Initialize Router with memoryLimit of 2.
router.addPacket(7, 4, 90); // Return True.
router.forwardPacket(); // Return [7, 4, 90].
router.forwardPacket(); // There are no packets left, return [].
 
Constraints:

2 <= memoryLimit <= 105
1 <= source, destination <= 2 * 105
1 <= timestamp <= 109
1 <= startTime <= endTime <= 109
At most 105 calls will be made to addPacket, forwardPacket, and getCount methods altogether.
queries for addPacket will be made in non-decreasing order of timestamp.
"""


from collections import deque, defaultdict
from bisect import bisect_left, bisect_right
from typing import List


class Router:

    def __init__(self, memory_limit: int):
        self.limit = memory_limit

        # FIFO storage of active packets
        self.q = deque()

        # Active packets only, for duplicate detection
        self.active = set()

        # destination -> all inserted timestamps for that destination
        self.times = defaultdict(list)

        # destination -> first active index in times[destination]
        self.left = defaultdict(int)

    def _remove_oldest(self) -> None:
        """Remove the oldest packet from the router."""
        s, d, t = self.q.popleft()
        self.active.remove((s, d, t))
        self.left[d] += 1

    def add_packet(self, source: int, destination: int, timestamp: int) -> bool:
        packet = (source, destination, timestamp)

        # Duplicate among currently stored packets
        if packet in self.active:
            return False

        # Add new packet
        self.q.append(packet)
        self.active.add(packet)
        self.times[destination].append(timestamp)

        # Enforce memory limit
        if len(self.q) > self.limit:
            self._remove_oldest()

        return True

    def forward_packet(self) -> List[int]:
        if not self.q:
            return []

        packet = self.q.popleft()
        self.active.remove(packet)

        s, d, t = packet
        self.left[d] += 1

        return [s, d, t]

    def get_count(self, destination: int, start_time: int, end_time: int) -> int:
        arr = self.times[destination]
        l = self.left[destination]

        # Search only in the active suffix arr[l:]
        lo = bisect_left(arr, start_time, l)
        hi = bisect_right(arr, end_time, l)

        return hi - lo
    
# Complexity analysis
"""
Let n be the number of calls to addPacket, forwardPacket, and getCount.
addPacket
Time: O(1) for adding, plus O(1) for duplicate check, plus O(1) for memory limit enforcement = O(1)
forwardPacket
Time: O(1) for removing from queue and set, plus O(1) for updating left pointer = O(1)
getCount
Time: O(log m) where m is the number of packets ever added with the given destination, due to binary search
Overall, each method runs in O(1) or O(log m) time, which is efficient for the given constraints.

Space complexity
O(n) for storing packets in the queue and set, plus O(n) for the times 
dictionary in the worst case where all packets have unique destinations.
"""
