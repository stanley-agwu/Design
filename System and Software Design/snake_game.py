# Snake Game

"""
Design a Snake game that is played on a device with screen size 
height x width. Play the game online if you are not familiar with the game.

The snake is initially positioned at the top left corner (0, 0) with a length 
of 1 unit.

You are given an array food where food[i] = (ri, ci) is the row and column 
position of a piece of food that the snake can eat. When a snake eats a piece
of food, its length and the game's score both increase by 1.

Each piece of food appears one by one on the screen, meaning the second piece
of food will not appear until the snake eats the first piece of food.

When a piece of food appears on the screen, it is guaranteed that it will 
not appear on a block occupied by the snake.

The game is over if the snake goes out of bounds (hits a wall) or if its 
head occupies a space that its body occupies after moving (i.e. a snake of length 4 cannot run into itself).

Implement the SnakeGame class:

SnakeGame(int width, int height, int[][] food) Initializes the object with a 
screen of size height x width and the positions of the food.
int move(String direction) Returns the score of the game after applying one 
direction move by the snake. If the game is over, return -1.

Example 1:

Input
["SnakeGame", "move", "move", "move", "move", "move", "move"]
[[3, 2, [[1, 2], [0, 1]]], ["R"], ["D"], ["R"], ["U"], ["L"], ["U"]]
Output
[null, 0, 0, 1, 1, 2, -1]

Explanation
SnakeGame snakeGame = new SnakeGame(3, 2, [[1, 2], [0, 1]]);
snakeGame.move("R"); // return 0
snakeGame.move("D"); // return 0
snakeGame.move("R"); // return 1, snake eats the first piece of food. The 
    second piece of food appears at (0, 1).
snakeGame.move("U"); // return 1
snakeGame.move("L"); // return 2, snake eats the second food. No more food appears.
snakeGame.move("U"); // return -1, game over because snake collides with border

Constraints:

1 <= width, height <= 104
1 <= food.length <= 50
food[i].length == 2
0 <= ri < height
0 <= ci < width
direction.length == 1
direction is 'U', 'D', 'L', or 'R'.
At most 104 calls will be made to move.
"""

# Idea

"""
Use a deque for the snake’s body in order from head to tail, and a hash set 
for O(1) collision checks.

The subtle part is self-collision: moving into the current tail cell is 
allowed if the snake is not eating food on that move, because the tail will 
move away first. So for a normal move, remove the tail from the set before 
checking collision.

We need these operations efficiently for every move:

-> compute new head position
-> detect wall collision
-> detect self collision
-> grow when food is eaten
-> otherwise move tail forward

Data structures
-> deque[(r, c)] for the snake body
    head at the front
    tail at the back
-> set[(r, c)] for occupied cells
-> food_index to track the next food to appear
"""

from collections import deque
from typing import List


class SnakeGame:

    def __init__(self, width: int, height: int, food: List[List[int]]):
        self.width = width
        self.height = height
        self.food = food
        self.food_index = 0
        self.score = 0
        self.game_over = False

        # Snake starts at (0, 0)
        self.snake = deque([(0, 0)])
        self.occupied = {(0, 0)}

        self.dirs = {
            "U": (-1, 0),
            "D": (1, 0),
            "L": (0, -1),
            "R": (0, 1),
        }

    def move(self, direction: str) -> int:
        if self.game_over:
            return -1

        head_r, head_c = self.snake[0]
        dr, dc = self.dirs[direction]
        new_r, new_c = head_r + dr, head_c + dc

        # 1. Check wall collision
        if not (0 <= new_r < self.height and 0 <= new_c < self.width):
            self.game_over = True
            return -1

        new_head = (new_r, new_c)

        # 2. Check whether this move eats food
        eating = (
            self.food_index < len(self.food)
            and [new_r, new_c] == self.food[self.food_index]
        )

        if eating:
            # Tail does NOT move, so any occupied cell is a collision
            if new_head in self.occupied:
                self.game_over = True
                return -1

            self.snake.appendleft(new_head)
            self.occupied.add(new_head)
            self.food_index += 1
            self.score += 1

        else:
            # Tail moves away, so remove it first
            tail = self.snake.pop()
            self.occupied.remove(tail)

            if new_head in self.occupied:
                self.game_over = True
                return -1

            self.snake.appendleft(new_head)
            self.occupied.add(new_head)

        return self.score
    
# Complexity Analysis
"""
Let n be the number of moves.
Time Complexity: O(1) for each move, since all operations (collision checks, 
    adding/removing from deque and set) are O(1).
Space Complexity: O(k) where k is the maximum length of the snake, which is
    at most the number of moves or the number of food items, whichever is smaller.
"""


