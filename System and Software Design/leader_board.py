# Design a LeaderBoard

"""
Design a Leaderboard class, which has 3 functions:

addScore(playerId, score): Update the leaderboard by adding score to the 
    given player's score. If there is no player with such id in the leaderboard, 
    add him to the leaderboard with the given score.
top(K): Return the score sum of the top K players.
reset(playerId): Reset the score of the player with the given id to 0 
    (in other words erase it from the leaderboard). It is guaranteed that 
    the player was added to the leaderboard before calling this function.
Initially, the leaderboard is empty.

Example 1:

Input: 
["Leaderboard","addScore","addScore","addScore","addScore","addScore","top","reset","reset","addScore","top"]
[[],[1,73],[2,56],[3,39],[4,51],[5,4],[1],[1],[2],[2,51],[3]]
Output: 
[null,null,null,null,null,null,73,null,null,null,141]

Explanation: 
Leaderboard leaderboard = new Leaderboard ();
leaderboard.addScore(1,73);   // leaderboard = [[1,73]];
leaderboard.addScore(2,56);   // leaderboard = [[1,73],[2,56]];
leaderboard.addScore(3,39);   // leaderboard = [[1,73],[2,56],[3,39]];
leaderboard.addScore(4,51);   // leaderboard = [[1,73],[2,56],[3,39],[4,51]];
leaderboard.addScore(5,4);    // leaderboard = [[1,73],[2,56],[3,39],[4,51],[5,4]];
leaderboard.top(1);           // returns 73;
leaderboard.reset(1);         // leaderboard = [[2,56],[3,39],[4,51],[5,4]];
leaderboard.reset(2);         // leaderboard = [[3,39],[4,51],[5,4]];
leaderboard.addScore(2,51);   // leaderboard = [[2,51],[3,39],[4,51],[5,4]];
leaderboard.top(3);           // returns 141 = 51 + 51 + 39;

Constraints:

1 <= playerId, K <= 10000
It's guaranteed that K is less than or equal to the current number of players.
1 <= score <= 100
There will be at most 1000 function calls.
"""

# Idea
"""
Use a hash map for each player’s current score, and compute top(K) from the scores.

Because there are at most 1000 calls total, a simple design is already efficient enough.
"""

class Leaderboard:

    def __init__(self):
        self.scores = {}

    def add_score(self, player_id: int, score: int) -> None:
        if player_id not in self.scores:
            self.scores[player_id] = 0
        self.scores[player_id] += score

    def top(self, k: int) -> int:
        all_scores = sorted(self.scores.values(), reverse=True)
        return sum(all_scores[:k])

    def reset(self, player_id: int) -> None:
        del self.scores[player_id]

# Time complexity:
"""
addScore: O(1)
top: O(n log n) where n is the number of players (sorting scores).
reset: O(1)

Space complexity: O(n) where n is the number of players (storing scores).
"""



