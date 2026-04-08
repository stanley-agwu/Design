# Walking Robot Simulation II

"""
A width x height grid is on an XY-plane with the bottom-left cell at (0, 0) and the top-right cell at (width - 1, height - 1). The grid is aligned with the four cardinal directions ("North", "East", "South", and "West"). A robot is initially at cell (0, 0) facing direction "East".

The robot can be instructed to move for a specific number of steps. For each step, it does the following.

Attempts to move forward one cell in the direction it is facing.
If the cell the robot is moving to is out of bounds, the robot instead turns 90 degrees counterclockwise and retries the step.
After the robot finishes moving the number of steps required, it stops and awaits the next instruction.

Implement the Robot class:

Robot(int width, int height) Initializes the width x height grid with the robot at (0, 0) facing "East".
void step(int num) Instructs the robot to move forward num steps.
int[] getPos() Returns the current cell the robot is at, as an array of length 2, [x, y].
String getDir() Returns the current direction of the robot, "North", "East", "South", or "West".
 

Example 1:

example-1
Input
["Robot", "step", "step", "getPos", "getDir", "step", "step", "step", "getPos", "getDir"]
[[6, 3], [2], [2], [], [], [2], [1], [4], [], []]
Output
[null, null, null, [4, 0], "East", null, null, null, [1, 2], "West"]

Explanation
Robot robot = new Robot(6, 3); // Initialize the grid and the robot at (0, 0) facing East.
robot.step(2);  // It moves two steps East to (2, 0), and faces East.
robot.step(2);  // It moves two steps East to (4, 0), and faces East.
robot.getPos(); // return [4, 0]
robot.getDir(); // return "East"
robot.step(2);  // It moves one step East to (5, 0), and faces East.
                // Moving the next step East would be out of bounds, so it turns and faces North.
                // Then, it moves one step North to (5, 1), and faces North.
robot.step(1);  // It moves one step North to (5, 2), and faces North (not West).
robot.step(4);  // Moving the next step North would be out of bounds, so it turns and faces West.
                // Then, it moves four steps West to (1, 2), and faces West.
robot.getPos(); // return [1, 2]
robot.getDir(); // return "West"

Constraints:

2 <= width, height <= 100
1 <= num <= 105
At most 104 calls in total will be made to step, getPos, and getDir.
"""

class Robot:

    def __init__(self, width: int, height: int):
        self.w = width
        self.h = height
        # Total steps to complete one full loop
        self.perimeter = 2 * (width + height - 2)
        # 1D position tracking
        self.pos = 0
        self.moved = False

    def step(self, num: int) -> None:
        self.moved = True
        # Modulo arithmetic completely bypasses the simulation
        self.pos = (self.pos + num) % self.perimeter

    def get_pos(self) -> list[int]:
        p = self.pos
        
        # 1. Bottom edge (Moving East)
        if p < self.w:
            return [p, 0]
        # 2. Right edge (Moving North)
        elif p < self.w + self.h - 1:
            return [self.w - 1, p - (self.w - 1)]
        # 3. Top edge (Moving West)
        elif p < 2 * self.w + self.h - 2:
            # Start at right edge, subtract the steps moved along the top
            return [(self.w - 1) - (p - (self.w + self.h - 2)), self.h - 1]
        # 4. Left edge (Moving South)
        else:
            # Start at top edge, subtract the steps moved down the left side
            # Fun fact: mathematically this simplifies beautifully to self.perimeter - p
            return [0, self.perimeter - p]

    def get_dir(self) -> str:
        p = self.pos
        
        # The Edge Case: (0, 0)
        if p == 0:
            return "South" if self.moved else "East"
            
        if p < self.w:
            return "East"
        elif p < self.w + self.h - 1:
            return "North"
        elif p < 2 * self.w + self.h - 2:
            return "West"
        else:
            return "South"
    
# Complexity Analysis
"""
__init__: O(1)
step(num): O(1)
get_pos(): O(1)
get_dir(): O(1)

Space complexity: O(1)
"""
