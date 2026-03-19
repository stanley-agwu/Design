# Design Task Manager

"""
There is a task management system that allows users to manage their tasks, each 
associated with a priority. The system should efficiently handle adding, 
modifying, executing, and removing tasks.

Implement the TaskManager class:

TaskManager(vector<vector<int>>& tasks) initializes the task manager with a list 
    of user-task-priority triples. Each element in the input list is of the form 
    [userId, taskId, priority], which adds a task to the specified user with the 
    given priority.

void add(int userId, int taskId, int priority) adds a task with the specified 
    taskId and priority to the user with userId. It is guaranteed that taskId 
    does not exist in the system.

void edit(int taskId, int newPriority) updates the priority of the existing 
    taskId to newPriority. It is guaranteed that taskId exists in the system.

void rmv(int taskId) removes the task identified by taskId from the system. 
    It is guaranteed that taskId exists in the system.

int execTop() executes the task with the highest priority across all users. 
If there are multiple tasks with the same highest priority, execute the one 
with the highest taskId. After executing, the taskId is removed from the system. 
Return the userId associated with the executed task. If no tasks are available, 
return -1.

Note that a user may be assigned multiple tasks.

 

Example 1:

Input:
["TaskManager", "add", "edit", "execTop", "rmv", "add", "execTop"]
[[[[1, 101, 10], [2, 102, 20], [3, 103, 15]]], [4, 104, 5], [102, 8], [], [101], 
[5, 105, 15], []]

Output:
[null, null, null, 3, null, null, 5]

Explanation

TaskManager taskManager = new TaskManager([[1, 101, 10], [2, 102, 20], 
    [3, 103, 15]]); // Initializes with three tasks for Users 1, 2, and 3.
taskManager.add(4, 104, 5); // Adds task 104 with priority 5 for User 4.
taskManager.edit(102, 8); // Updates priority of task 102 to 8.
taskManager.execTop(); // return 3. Executes task 103 for User 3.
taskManager.rmv(101); // Removes task 101 from the system.
taskManager.add(5, 105, 15); // Adds task 105 with priority 15 for User 5.
taskManager.execTop(); // return 5. Executes task 105 for User 5.
 

Constraints:

1 <= tasks.length <= 105
0 <= userId <= 105
0 <= taskId <= 105
0 <= priority <= 109
0 <= newPriority <= 109
At most 2 * 105 calls will be made in total to add, edit, rmv, and execTop methods.
The input is generated such that taskId will be valid.
"""

# Idea
"""
Use a max-heap + hash map with lazy deletion.

That gives:
    add → O(log n)
    edit → O(log n)
    rmv → O(1)
    execTop → amortized O(log n)

Idea

We need to always execute:
1. the highest priority
2. if tied, the highest taskId

But tasks can also be edited and removed.
A plain heap alone is not enough, because:
-> edit(taskId, newPriority) changes an existing task already inside the heap
-> rmv(taskId) removes an arbitrary task, which heaps do not support efficiently

So we use:
-> a hash map taskInfo[taskId] = {userId, priority}
-> a max-heap storing entries (priority, taskId, userId)

# Lazy deletion
When a task is edited:
-> update taskInfo[taskId]
-> push the new version into the heap

When a task is removed:
-> erase it from taskInfo

When taking the top from the heap:
-> keep popping while the heap entry is stale

an entry is stale if:
-> its taskId no longer exists in taskInfo, or
-> its priority/userId no longer matches the current task info

This avoids expensive heap deletions.
"""
# Use Priority Queue with Lazy deletion
import heapq


class TaskManager:
    def __init__(self, tasks: list[list[int]]):
        self.task_info = {}   # taskId -> (userId, priority)
        self.heap = []        # max-heap simulated with (-priority, -taskId, userId)

        for user_id, task_id, priority in tasks:
            self.task_info[task_id] = (user_id, priority)
            heapq.heappush(self.heap, (-priority, -task_id, user_id))

    def add(self, user_id: int, task_id: int, priority: int) -> None:
        self.task_info[task_id] = (user_id, priority)
        heapq.heappush(self.heap, (-priority, -task_id, user_id))

    def edit(self, task_id: int, new_priority: int) -> None:
        user_id, _ = self.task_info[task_id]
        self.task_info[task_id] = (user_id, new_priority)
        heapq.heappush(self.heap, (-new_priority, -task_id, user_id))

    def rmv(self, task_id: int) -> None:
        del self.task_info[task_id]

    def exec_top(self) -> int:
        while self.heap:
            neg_priority, neg_task_id, user_id = heapq.heappop(self.heap)
            priority = -neg_priority
            task_id = -neg_task_id

            if task_id not in self.task_info:
                continue

            current_user, current_priority = self.task_info[task_id]
            if current_user != user_id or current_priority != priority:
                continue

            del self.task_info[task_id]
            return user_id

        return -1
    
# Time complexity
# add: O(log n)
# edit: O(log n)
# rmv: O(1)
# execTop: amortized O(log n)

# O(n) - Space complexity


# Use SortedContainers' SortedList
from sortedcontainers import SortedList

class TaskManager2:
    def __init__(self, tasks: list[list[int]]):
        self.task_info = {}   # taskId -> (userId, priority)
        self.sorted_list = SortedList() # sorted list of (priority, taskId, userId)

        for user_id, task_id, priority in tasks:
            self.task_info[task_id] = (user_id, priority)
            self.sorted_list.add((priority, task_id, user_id))

    def add(self, user_id: int, task_id: int, priority: int) -> None:
        self.task_info[task_id] = (user_id, priority)
        self.sorted_list.add((priority, task_id, user_id))

    def edit(self, task_id: int, new_priority: int) -> None:
        user_id, old_priority = self.task_info[task_id]
        self.task_info[task_id] = (user_id, new_priority)
        self.sorted_list.discard((old_priority, task_id, user_id))
        self.sorted_list.add((new_priority, task_id, user_id))

    def rmv(self, task_id: int) -> None:
        priority, user_id = self.task_info[task_id]
        del self.task_info[task_id]
        self.sorted_list.discard(priority, task_id, user_id)

    def exec_top(self) -> int:
        if not self.sorted_list:
            return -1
        _, _, user_id = self.sorted_list.pop()
        return user_id
    
# Time complexity
# add: O(n)
# edit: O(n)
# rmv: O(n)
# execTop: O(n)

# O(n) - Space complexity