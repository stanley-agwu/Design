# Design File System

"""
You are asked to design a file system that allows you to create new paths and 
associate them with different values.

The format of a path is one or more concatenated strings of the form: / followed 
by one or more lowercase English letters. For example, "/leetcode" and 
"/leetcode/problems" are valid paths while an empty string "" and "/" are not.

Implement the FileSystem class:

bool createPath(string path, int value) Creates a new path and associates a 
value to it if possible and returns true. Returns false if the path already 
exists or its parent path doesn't exist.
int get(string path) Returns the value associated with path or returns -1 if 
the path doesn't exist.

Example 1:

Input: 
["FileSystem","createPath","get"]
[[],["/a",1],["/a"]]
Output: 
[null,true,1]
Explanation: 
FileSystem fileSystem = new FileSystem();

fileSystem.createPath("/a", 1); // return true
fileSystem.get("/a"); // return 1
Example 2:

Input: 
["FileSystem","createPath","createPath","get","createPath","get"]
[[],["/leet",1],["/leet/code",2],["/leet/code"],["/c/d",1],["/c"]]
Output: 
[null,true,true,2,false,-1]
Explanation: 
FileSystem fileSystem = new FileSystem();

fileSystem.createPath("/leet", 1); // return true
fileSystem.createPath("/leet/code", 2); // return true
fileSystem.get("/leet/code"); // return 2
fileSystem.createPath("/c/d", 1); // return false because the parent path 
"/c" doesn't exist.
fileSystem.get("/c"); // return -1 because this path doesn't exist.

Constraints:

2 <= path.length <= 100
1 <= value <= 109
Each path is valid and consists of lowercase English letters and '/'.
At most 104 calls in total will be made to createPath and get.
"""

# Idea
"""
Use a hash map from full path string to its value.

The only tricky part is createPath:

-> the path must not already exist
-> its parent must already exist
-> for a top-level path like "/a", the parent is the virtual root ""
"""

class FileSystem:

    def __init__(self):
        self.paths = {"": -1}  # virtual root

    def create_path(self, path: str, value: int) -> bool:
        if path in self.paths:
            return False

        idx = path.rfind("/")
        parent = path[:idx]

        if parent not in self.paths:
            return False

        self.paths[path] = value
        return True

    def get(self, path: str) -> int:
        return self.paths.get(path, -1)
    
# Time complexity:
"""
createPath: O(1) average time (hash map lookup and insert).
get: O(1) average time (hash map lookup).
"""

# Space complexity:
"""
O(n) where n is the number of created paths (storing paths in hash map).
"""


