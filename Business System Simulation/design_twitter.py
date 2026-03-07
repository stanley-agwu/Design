# Design Twitter

"""
Design a simplified version of Twitter where users can post tweets, 
follow/unfollow another user, and is able to see the 10 most recent 
tweets in the user's news feed.

Implement the Twitter class:

Twitter() Initializes your twitter object.
void postTweet(int userId, int tweetId) Composes a new tweet with ID 
    tweetId by the user userId. Each call to this function will be made 
    with a unique tweetId.
List<Integer> getNewsFeed(int userId) Retrieves the 10 most recent tweet 
    IDs in the user's news feed. Each item in the news feed must be posted 
    by users who the user followed or by the user themself. Tweets must be 
    ordered from most recent to least recent.
void follow(int followerId, int followeeId) The user with ID followerId 
    started following the user with ID followeeId.
void unfollow(int followerId, int followeeId) The user with ID followerId 
    started unfollowing the user with ID followeeId.
 

Example 1:

Input
["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"]
[[], [1, 5], [1], [1, 2], [2, 6], [1], [1, 2], [1]]
Output
[null, null, [5], null, null, [6, 5], null, [5]]

Explanation
Twitter twitter = new Twitter();
twitter.postTweet(1, 5); // User 1 posts a new tweet (id = 5).
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 1 tweet id -> [5]. return [5]
twitter.follow(1, 2);    // User 1 follows user 2.
twitter.postTweet(2, 6); // User 2 posts a new tweet (id = 6).
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 2 tweet ids -> [6, 5]. Tweet id 6 should precede tweet id 5 because it is posted after tweet id 5.
twitter.unfollow(1, 2);  // User 1 unfollows user 2.
twitter.getNewsFeed(1);  // User 1's news feed should return a list with 1 tweet id -> [5], since user 1 is no longer following user 2.
 

Constraints:

1 <= userId, followerId, followeeId <= 500
0 <= tweetId <= 104
All the tweets have unique IDs.
At most 3 * 104 calls will be made to postTweet, getNewsFeed, follow, and unfollow.
A user cannot follow himself.
"""

from collections import defaultdict
import heapq


class Twitter:

    def __init__(self):
        self.time = 0
        self.follow_map = defaultdict(set)   # follower -> set of followees
        self.tweets = defaultdict(list)      # user -> list of (time, tweetId)

    def post_tweet(self, user_id: int, tweet_id: int) -> None:
        self.time += 1
        self.tweets[user_id].append((self.time, tweet_id))

    def get_news_feed(self, user_id: int) -> list[int]:
        result = []
        max_heap = []

        users = set(self.follow_map[user_id])
        users.add(user_id)  # user always sees own tweets

        # Push each user's most recent tweet into heap
        for user in users:
            if self.tweets[user]:
                idx = len(self.tweets[user]) - 1
                time, tweet_id = self.tweets[user][idx]
                # use negative time because heapq is a min-heap
                heapq.heappush(max_heap, (-time, tweet_id, user, idx))

        # Extract up to 10 most recent tweets
        while max_heap and len(result) < 10:
            _, tweet_id, user, idx = heapq.heappop(max_heap)
            result.append(tweet_id)

            # Push the previous tweet from the same user
            if idx > 0:
                prev_time, prev_tweet_id = self.tweets[user][idx - 1]
                heapq.heappush(max_heap, (-prev_time, prev_tweet_id, user, idx - 1))

        return result

    def follow(self, follower_id: int, followee_id: int) -> None:
        if follower_id != followee_id:
            self.follow_map[follower_id].add(followee_id)

    def unfollow(self, follower_id: int, followee_id: int) -> None:
        self.follow_map[follower_id].discard(followee_id)


# Let f be the number of followed users plus the user themself.
# pushing initial latest tweets: O(f log f)
# extracting at most 10 tweets: O(10 log f)

# So overall:

# Time: O(f log f)
# Space: O(f)

twitter = Twitter()
twitter.post_tweet(1, 5)
print(twitter.get_news_feed(1))
twitter.follow(1, 2)
twitter.post_tweet(2, 6)
print(twitter.get_news_feed(1))
twitter.unfollow(1, 2)
print(twitter.get_news_feed(1))