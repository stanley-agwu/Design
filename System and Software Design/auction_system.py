# Design Auction System

"""
You are asked to design an auction system that manages bids from multiple 
users in real time.

Each bid is associated with a userId, an itemId, and a bidAmount.

Implement the AuctionSystem class:​​​​​​​

AuctionSystem(): Initializes the AuctionSystem object.
void addBid(int userId, int itemId, int bidAmount): Adds a new bid for itemId 
    by userId with bidAmount. If the same userId already has a bid on itemId, 
    replace it with the new bidAmount.
void updateBid(int userId, int itemId, int newAmount): Updates the existing 
    bid of userId for itemId to newAmount. It is guaranteed that this bid exists.
void removeBid(int userId, int itemId): Removes the bid of userId for itemId. 
    It is guaranteed that this bid exists.
int getHighestBidder(int itemId): Returns the userId of the highest bidder 
    for itemId. If multiple users have the same highest bidAmount, return 
    the user with the highest userId. If no bids exist for the item, return -1.
 

Example 1:

Input:
["AuctionSystem", "addBid", "addBid", "getHighestBidder", "updateBid", "getHighestBidder", "removeBid", "getHighestBidder", "getHighestBidder"]
[[], [1, 7, 5], [2, 7, 6], [7], [1, 7, 8], [7], [2, 7], [7], [3]]

Output:
[null, null, null, 2, null, 1, null, 1, -1]

Explanation

AuctionSystem auctionSystem = new AuctionSystem(); // Initialize the Auction system
auctionSystem.addBid(1, 7, 5); // User 1 bids 5 on item 7
auctionSystem.addBid(2, 7, 6); // User 2 bids 6 on item 7
auctionSystem.getHighestBidder(7); // return 2 as User 2 has the highest bid
auctionSystem.updateBid(1, 7, 8); // User 1 updates bid to 8 on item 7
auctionSystem.getHighestBidder(7); // return 1 as User 1 now has the highest bid
auctionSystem.removeBid(2, 7); // Remove User 2's bid on item 7
auctionSystem.getHighestBidder(7); // return 1 as User 1 is the current highest 
bidder
auctionSystem.getHighestBidder(3); // return -1 as no bids exist for item 3
 

Constraints:

1 <= userId, itemId <= 5 * 104
1 <= bidAmount, newAmount <= 109
At most 5 * 104 total calls to addBid, updateBid, removeBid, and getHighestBidder.
The input is generated such that for updateBid and removeBid, the bid from the 
given userId for the given itemId will be valid.
"""

import heapq
from collections import defaultdict

class AuctionSystem:

    def __init__(self):
        # itemId -> {userId: bidAmount}
        self.bids = defaultdict(dict)
        
        # itemId -> heap of (-bidAmount, -userId)
        self.heaps = defaultdict(list)

    def add_bid(self, user_id: int, item_id: int, bid_amount: int) -> None:
        self.bids[item_id][user_id] = bid_amount
        heapq.heappush(self.heaps[item_id], (-bid_amount, -user_id))

    def update_bid(self, user_id: int, item_id: int, new_amount: int) -> None:
        self.bids[item_id][user_id] = new_amount
        heapq.heappush(self.heaps[item_id], (-new_amount, -user_id))

    def remove_bid(self, user_id: int, item_id: int) -> None:
        del self.bids[item_id][user_id]

    def get_highest_bidder(self, item_id: int) -> int:
        heap = self.heaps[item_id]
        current_bids = self.bids[item_id]

        while heap:
            neg_amount, neg_user = heap[0]
            amount = -neg_amount
            user = -neg_user

            # valid only if this matches the current live bid
            if user in current_bids and current_bids[user] == amount:
                return user

            heapq.heappop(heap)  # discard stale entry

        return -1
    
# Complexity analysis
"""
Let k be the number of bids ever pushed for a given item.
-> addBid: O(log k)
-> updateBid: O(log k)
-> removeBid: O(1)
-> getHighestBidder: amortized O(log k)

Why amortized?
Each stale heap entry is popped at most once over the whole execution.

Space
O(total number of add/update pushes), at most O(5 * 10^4)
"""