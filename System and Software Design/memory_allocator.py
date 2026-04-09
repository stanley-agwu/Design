# Design Memory Allocator

"""
You are given an integer n representing the size of a 0-indexed memory array. All memory units are initially free.

You have a memory allocator with the following functionalities:

Allocate a block of size consecutive free memory units and assign it the id m_id.
Free all memory units with the given id m_id.
Note that:

Multiple blocks can be allocated to the same m_id.
You should free all the memory units with m_id, even if they were allocated in different blocks.
Implement the Allocator class:

Allocator(int n) Initializes an Allocator object with a memory array of size n.
int allocate(int size, int m_id) Find the leftmost block of size consecutive free memory units and allocate it with the id m_id. Return the block's first index. If such a block does not exist, return -1.
int freeMemory(int m_id) Free all memory units with the id m_id. Return the number of memory units you have freed.
 

Example 1:

Input
["Allocator", "allocate", "allocate", "allocate", "freeMemory", "allocate", "allocate", "allocate", "freeMemory", "allocate", "freeMemory"]
[[10], [1, 1], [1, 2], [1, 3], [2], [3, 4], [1, 1], [1, 1], [1], [10, 2], [7]]
Output
[null, 0, 1, 2, 1, 3, 1, 6, 3, -1, 0]

Explanation
Allocator loc = new Allocator(10); // Initialize a memory array of size 10. All memory units are initially free.
loc.allocate(1, 1); // The leftmost block's first index is 0. The memory array becomes [1,_,_,_,_,_,_,_,_,_]. We return 0.
loc.allocate(1, 2); // The leftmost block's first index is 1. The memory array becomes [1,2,_,_,_,_,_,_,_,_]. We return 1.
loc.allocate(1, 3); // The leftmost block's first index is 2. The memory array becomes [1,2,3,_,_,_,_,_,_,_]. We return 2.
loc.freeMemory(2); // Free all memory units with m_id 2. The memory array becomes [1,_, 3,_,_,_,_,_,_,_]. We return 1 since there is only 1 unit with m_id 2.
loc.allocate(3, 4); // The leftmost block's first index is 3. The memory array becomes [1,_,3,4,4,4,_,_,_,_]. We return 3.
loc.allocate(1, 1); // The leftmost block's first index is 1. The memory array becomes [1,1,3,4,4,4,_,_,_,_]. We return 1.
loc.allocate(1, 1); // The leftmost block's first index is 6. The memory array becomes [1,1,3,4,4,4,1,_,_,_]. We return 6.
loc.freeMemory(1); // Free all memory units with m_id 1. The memory array becomes [_,_,3,4,4,4,_,_,_,_]. We return 3 since there are 3 units with m_id 1.
loc.allocate(10, 2); // We can not find any free block with 10 consecutive free memory units, so we return -1.
loc.freeMemory(7); // Free all memory units with m_id 7. The memory array remains the same since there is no memory unit with m_id 7. We return 0.
 

Constraints:

1 <= n, size, m_id <= 1000
At most 1000 calls will be made to allocate and freeMemory.
"""

class Allocator:

    def __init__(self, n: int):
        # 0 means free
        self.memory = [0] * n

    def allocate(self, size: int, m_id: int) -> int:
        n = len(self.memory)
        free_count = 0
        start = 0

        for i in range(n):
            if self.memory[i] == 0:
                if free_count == 0:
                    start = i
                free_count += 1

                if free_count == size:
                    for j in range(start, start + size):
                        self.memory[j] = m_id
                    return start
            else:
                free_count = 0

        return -1

    def free_memory(self, m_id: int) -> int:
        freed = 0

        for i in range(len(self.memory)):
            if self.memory[i] == m_id:
                self.memory[i] = 0
                freed += 1

        return freed
    
# Time complexity:
# allocate: O(n) in the worst case when we have to scan the entire memory array
# free_memory: O(n) in the worst case when all memory units have the same m_id

# Space complexity:
# O(n) for storing the memory array of size n
