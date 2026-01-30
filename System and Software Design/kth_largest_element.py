# Kth Largest Element in a Stream

# Implement a class which, for a given integer k, maintains a stream of 
# test scores and continuously returns the kth highest test score after 
# a new score has been submitted. More specifically, we are looking for 
# the kth highest score in the sorted list of all scores.

import heapq

class KthLargestScore:

    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = []
        for num in nums:
            self.add(num) # Reusable logic
        
    def add(self, val: int) -> int:
        heapq.heappush(self.nums, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.h[0]
