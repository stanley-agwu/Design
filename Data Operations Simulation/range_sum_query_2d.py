# Range Sum Query 2D - Immutable

"""
Given a 2D matrix matrix, handle multiple queries of the following type:
Calculate the sum of the elements of matrix inside the rectangle defined
by its upper left corner (row1, col1) and lower right corner (row2, col2).

Implement the NumMatrix class:
- NumMatrix(int[][] matrix) Initializes the object with the integer matrix matrix.
- int sumRegion(int row1, int col1, int row2, int col2) Returns the sum of the 
    elements of matrix inside the rectangle defined by its upper left corner 
    (row1, col1) and lower right corner (row2, col2).

You must design an algorithm where sumRegion works on O(1) time complexity.

Example 1:

Input
["NumMatrix", "sumRegion", "sumRegion", "sumRegion"]
[[[[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]], [2, 1, 4, 3], [1, 1, 2, 2], [1, 2, 2, 4]]
Output
[null, 8, 11, 12]

Explanation
NumMatrix numMatrix = new NumMatrix([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]);
numMatrix.sumRegion(2, 1, 4, 3); // return 8 (i.e sum of the red rectangle)
numMatrix.sumRegion(1, 1, 2, 2); // return 11 (i.e sum of the green rectangle)
numMatrix.sumRegion(1, 2, 2, 4); // return 12 (i.e sum of the blue rectangle)

Constraints:
- m == matrix.length
- n == matrix[i].length
- 0 <= row1 <= row2 < m
- 0 <= col1 <= col2 < n
- At most 104 calls will be made to sumRegion.
"""

# Idea:
"""
Use a 2D prefix sum.

That gives:
-> Preprocessing: O(m * n)
-> Each sumRegion: O(1)
-> Extra space: O(m * n)

For each cell, store the sum of all elements from (0,0) to that cell.
Let pref[r][c] represent the sum of the rectangle from the top-left corner 
to (r-1, c-1) in the original matrix.

Using a prefix matrix with one extra row and column makes boundary handling 
much cleaner.

Formula to build prefix sum ->
For 1 <= r <= m, 1 <= c <= n:

pref[r][c] = matrix[r-1][c-1] + pref[r-1][c] + pref[r][c-1] - pref[r-1][c-1]
To calculate the sum of a submatrix defined by (row1, col1) and (row2, col2):
sumRegion = pref[row2 + 1][col2 + 1] - pref[row1][col2 + 1] - pref[row2 + 1][col1] + pref[row1][col1]

"""

class NumMatrix:

    def __init__(self, matrix: list[list[int]]):
        m, n = len(matrix), len(matrix[0])

        # prefix sum matrix with 1 extra row and column
        self.pref = [[0] * (n + 1) for _ in range(m + 1)]

        for r in range(1, m + 1):
            for c in range(1, n + 1):
                self.pref[r][c] = (
                    matrix[r - 1][c - 1]
                    + self.pref[r - 1][c]
                    + self.pref[r][c - 1]
                    - self.pref[r - 1][c - 1]
                )

    def sum_region(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (
            self.pref[row2 + 1][col2 + 1]
            - self.pref[row1][col2 + 1]
            - self.pref[row2 + 1][col1]
            + self.pref[row1][col1]
        )

# Complexity Analysis:
# Constructor: O(m * n)
# sum_region: O(1)
# Space: O(m * n)