# Range Sum Query 2D - Mutable

"""
Given a 2D matrix matrix, handle multiple queries of the following types:

Update the value of a cell in matrix.
Calculate the sum of the elements of matrix inside the rectangle defined by its 
upper left corner (row1, col1) and lower right corner (row2, col2).
Implement the NumMatrix class:

NumMatrix(int[][] matrix) Initializes the object with the integer matrix matrix.
void update(int row, int col, int val) Updates the value of matrix[row][col] to be val.
int sumRegion(int row1, int col1, int row2, int col2) Returns the sum of the 
elements of matrix inside the rectangle defined by its upper left corner 
(row1, col1) and lower right corner (row2, col2).

Example 1:

Input
["NumMatrix", "sumRegion", "update", "sumRegion"]
[[[[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]], [2, 1, 4, 3], [3, 2, 2], [2, 1, 4, 3]]
Output
[null, 8, null, 10]

Explanation
NumMatrix numMatrix = new NumMatrix([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]);
numMatrix.sumRegion(2, 1, 4, 3); // return 8 (i.e. sum of the left red rectangle)
numMatrix.update(3, 2, 2);       // matrix changes from left image to right image
numMatrix.sumRegion(2, 1, 4, 3); // return 10 (i.e. sum of the right red rectangle)

Constraints:

m == matrix.length
n == matrix[i].length
1 <= m, n <= 200
-1000 <= matrix[i][j] <= 1000
0 <= row < m
0 <= col < n
-1000 <= val <= 1000
0 <= row1 <= row2 < m
0 <= col1 <= col2 < n
At most 5000 calls will be made to sumRegion and update.
"""

# Idea:
"""
Use a 2D Fenwick Tree (Binary Indexed Tree) for efficient updates and prefix sum queries.
This allows:
-> Preprocessing: O(m * n)
-> Each update: O(log m * log n)
-> Each sumRegion: O(log m * log n)
-> Extra space: O(m * n)
"""

class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        if not matrix or not matrix[0]:
            self.m = 0
            self.n = 0
            self.matrix = []
            self.bit = []
            return

        self.m = len(matrix)
        self.n = len(matrix[0])

        # Store the current matrix values so update() can compute delta.
        self.matrix = [[0] * self.n for _ in range(self.m)]

        # 2D Fenwick Tree uses 1-based indexing.
        self.bit = [[0] * (self.n + 1) for _ in range(self.m + 1)]

        # Build the structure by inserting each value.
        for r in range(self.m):
            for c in range(self.n):
                self.update(r, c, matrix[r][c])

    def _add(self, row: int, col: int, delta: int) -> None:
        """Add delta to cell (row, col) in the Fenwick tree."""
        i = row + 1
        while i <= self.m:
            j = col + 1
            while j <= self.n:
                self.bit[i][j] += delta
                j += j & -j
            i += i & -i

    def _prefix_sum(self, row: int, col: int) -> int:
        """Return sum of rectangle from (0,0) to (row,col), inclusive."""
        if row < 0 or col < 0:
            return 0

        total = 0
        i = row + 1
        while i > 0:
            j = col + 1
            while j > 0:
                total += self.bit[i][j]
                j -= j & -j
            i -= i & -i
        return total

    def update(self, row: int, col: int, val: int) -> None:
        delta = val - self.matrix[row][col]
        self.matrix[row][col] = val
        self._add(row, col, delta)

    def sum_region(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (
            self._prefix_sum(row2, col2)
            - self._prefix_sum(row1 - 1, col2)
            - self._prefix_sum(row2, col1 - 1)
            + self._prefix_sum(row1 - 1, col1 - 1)
        )
    
# Complexity Analysis:
"""
Time Complexity:
- Initialization: O(m * n) to build the Fenwick tree.
- update: O(log m * log n) to update the Fenwick tree.
- sumRegion: O(log m * log n) to compute the prefix sums and combine them.
Space Complexity:
- O(m * n) for the Fenwick tree and the matrix copy.
"""
