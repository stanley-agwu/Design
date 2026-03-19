# Design a Food Rating System

"""
Design a food rating system that can do the following:

Modify the rating of a food item listed in the system.
Return the highest-rated food item for a type of cuisine in the system.
Implement the FoodRatings class:

FoodRatings(String[] foods, String[] cuisines, int[] ratings) Initializes 
the system. The food items are described by foods, cuisines and ratings, 
all of which have a length of n.

foods[i] is the name of the ith food,
cuisines[i] is the type of cuisine of the ith food, and
ratings[i] is the initial rating of the ith food.
void changeRating(String food, int newRating) Changes the rating of the food 
    item with the name food.
String highestRated(String cuisine) Returns the name of the food item that 
    has the highest rating for the given type of cuisine. If there is a tie, 
    return the item with the lexicographically smaller name.
Note that a string x is lexicographically smaller than string y if x comes 
    before y in dictionary order, that is, either x is a prefix of y, or 
    if i is the first position such that x[i] != y[i], then x[i] comes 
    before y[i] in alphabetic order.

Example 1:

Input
["FoodRatings", "highestRated", "highestRated", "changeRating", "highestRated", 
    "changeRating", "highestRated"]
[[["kimchi", "miso", "sushi", "moussaka", "ramen", "bulgogi"], ["korean", 
    "japanese", "japanese", "greek", "japanese", "korean"], [9, 12, 8, 15, 14, 7]], 
    ["korean"], ["japanese"], ["sushi", 16], ["japanese"], ["ramen", 16], 
    ["japanese"]]
Output
[null, "kimchi", "ramen", null, "sushi", null, "ramen"]

Explanation
FoodRatings foodRatings = new FoodRatings(["kimchi", "miso", "sushi", "moussaka", "ramen", "bulgogi"], 
    ["korean", "japanese", "japanese", "greek", "japanese", "korean"], [9, 12, 8, 15, 14, 7]);
foodRatings.highestRated("korean"); // return "kimchi"
                                    // "kimchi" is the highest rated korean food with a rating of 9.
foodRatings.highestRated("japanese"); // return "ramen"
                                      // "ramen" is the highest rated japanese food with a rating of 14.
foodRatings.changeRating("sushi", 16); // "sushi" now has a rating of 16.
foodRatings.highestRated("japanese"); // return "sushi"
                                      // "sushi" is the highest rated japanese food with a rating of 16.
foodRatings.changeRating("ramen", 16); // "ramen" now has a rating of 16.
foodRatings.highestRated("japanese"); // return "ramen"
                                      // Both "sushi" and "ramen" have a rating of 16.
                                      // However, "ramen" is lexicographically smaller than "sushi".
 

Constraints:

1 <= n <= 2 * 104
n == foods.length == cuisines.length == ratings.length
1 <= foods[i].length, cuisines[i].length <= 10
foods[i], cuisines[i] consist of lowercase English letters.
1 <= ratings[i] <= 108
All the strings in foods are distinct.
food will be the name of a food item in the system across all calls to changeRating.
cuisine will be a type of cuisine of at least one food item in the system 
    across all calls to highestRated.
At most 2 * 104 calls in total will be made to changeRating and highestRated.
"""

import heapq
from collections import defaultdict


class FoodRatings:

    def __init__(self, foods: list[str], cuisines: list[str], ratings: list[int]):
        # food -> (cuisine, current_rating)
        self.food_info = {}

        # cuisine -> heap of (-rating, food)
        self.cuisine_heaps = defaultdict(list)

        for food, cuisine, rating in zip(foods, cuisines, ratings):
            self.food_info[food] = (cuisine, rating)
            heapq.heappush(self.cuisine_heaps[cuisine], (-rating, food))

    def change_rating(self, food: str, new_rating: int) -> None:
        cuisine, _ = self.food_info[food]
        self.food_info[food] = (cuisine, new_rating)
        heapq.heappush(self.cuisine_heaps[cuisine], (-new_rating, food))

    def highest_rated(self, cuisine: str) -> str:
        heap = self.cuisine_heaps[cuisine]

        while True:
            neg_rating, food = heap[0]
            current_cuisine, current_rating = self.food_info[food]

            # If heap top matches the latest rating, it's valid
            if current_cuisine == cuisine and -neg_rating == current_rating:
                return food

            # Otherwise discard stale entry
            heapq.heappop(heap)

# Time complexity
"""
-> __init__ O(n log n) 
-> changeRating O(log n)
-> highestRated O(log n)
"""

# Space complexity
"""
-> food_info: O(n)
-> heaps: original entries + updated entries
total O(n + number_of_updates)

So overall: O(n + q) where q is number of changeRating calls.
"""