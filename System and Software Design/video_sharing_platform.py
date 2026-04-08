# Design Video Sharing Platform

"""
You have a video sharing platform where users can upload and delete videos. 
Each video is a string of digits, where the ith digit of the string represents 
the content of the video at minute i. For example, the first digit represents 
the content at minute 0 in the video, the second digit represents the 
content at minute 1 in the video, and so on. Viewers of videos can also 
like and dislike videos. Internally, the platform keeps track of the number 
of views, likes, and dislikes on each video.

When a video is uploaded, it is associated with the smallest available 
integer videoId starting from 0. Once a video is deleted, the videoId 
associated with that video can be reused for another video.

Implement the VideoSharingPlatform class:

VideoSharingPlatform() Initializes the object.
int upload(String video) The user uploads a video. Return the videoId 
    associated with the video.
void remove(int videoId) If there is a video associated with videoId, 
    remove the video.
String watch(int videoId, int startMinute, int endMinute) If there is a 
    video associated with videoId, increase the number of views on the video by 1 and return the substring of the video string starting at startMinute and ending at min(endMinute, video.length - 1) (inclusive). Otherwise, return "-1".
void like(int videoId) Increases the number of likes on the video associated 
    with videoId by 1 if there is a video associated with videoId.
void dislike(int videoId) Increases the number of dislikes on the video 
    associated with videoId by 1 if there is a video associated with videoId.
int[] getLikesAndDislikes(int videoId) Return a 0-indexed integer array 
    values of length 2 where values[0] is the number of likes and values[1] is the number of dislikes on the video associated with videoId. If there is no video associated with videoId, return [-1].
int getViews(int videoId) Return the number of views on the video associated 
    with videoId, if there is no video associated with videoId, return -1.
 
Example 1:

Input
["VideoSharingPlatform", "upload", "upload", "remove", "remove", "upload", 
    "watch", "watch", "like", "dislike", "dislike", "getLikesAndDislikes", "getViews"]
[[], ["123"], ["456"], [4], [0], ["789"], [1, 0, 5], [1, 0, 1], [1], [1], [1], [1], [1]]
Output
[null, 0, 1, null, null, 0, "456", "45", null, null, null, [1, 2], 2]

Explanation
VideoSharingPlatform videoSharingPlatform = new VideoSharingPlatform();
videoSharingPlatform.upload("123");          // The smallest available videoId is 0, so return 0.
videoSharingPlatform.upload("456");          // The smallest available videoId is 1, so return 1.
videoSharingPlatform.remove(4);              // There is no video associated with videoId 4, so do nothing.
videoSharingPlatform.remove(0);              // Remove the video associated with videoId 0.
videoSharingPlatform.upload("789");          // Since the video associated with videoId 0 was deleted,
                                             // 0 is the smallest available videoId, so return 0.
videoSharingPlatform.watch(1, 0, 5);         // The video associated with videoId 1 is "456".
                                             // The video from minute 0 to min(5, 3 - 1) = 2 is "456", so return "456".
videoSharingPlatform.watch(1, 0, 1);         // The video associated with videoId 1 is "456".
                                             // The video from minute 0 to min(1, 3 - 1) = 1 is "45", so return "45".
videoSharingPlatform.like(1);                // Increase the number of likes on the video associated with videoId 1.
videoSharingPlatform.dislike(1);             // Increase the number of dislikes on the video associated with videoId 1.
videoSharingPlatform.dislike(1);             // Increase the number of dislikes on the video associated with videoId 1.
videoSharingPlatform.getLikesAndDislikes(1); // There is 1 like and 2 dislikes on the video associated with videoId 1, so return [1, 2].
videoSharingPlatform.getViews(1);            // The video associated with videoId 1 has 2 views, so return 2.
Example 2:

Input
["VideoSharingPlatform", "remove", "watch", "like", "dislike", "getLikesAndDislikes", "getViews"]
[[], [0], [0, 0, 1], [0], [0], [0], [0]]
Output
[null, null, "-1", null, null, [-1], -1]

Explanation
VideoSharingPlatform videoSharingPlatform = new VideoSharingPlatform();
videoSharingPlatform.remove(0);              // There is no video associated with videoId 0, so do nothing.
videoSharingPlatform.watch(0, 0, 1);         // There is no video associated with videoId 0, so return "-1".
videoSharingPlatform.like(0);                // There is no video associated with videoId 0, so do nothing.
videoSharingPlatform.dislike(0);             // There is no video associated with videoId 0, so do nothing.
videoSharingPlatform.getLikesAndDislikes(0); // There is no video associated with videoId 0, so return [-1].
videoSharingPlatform.getViews(0);            // There is no video associated with videoId 0, so return -1.
 

Constraints:

1 <= video.length <= 105
The sum of video.length over all calls to upload does not exceed 105
video consists of digits.
0 <= videoId <= 105
0 <= startMinute < endMinute < 105
startMinute < video.length
The sum of endMinute - startMinute over all calls to watch does not exceed 105.
At most 105 calls in total will be made to all functions.
"""

# Idea
"""
Use a hash map for active videos and a min-heap for reusable deleted ids.

That gives:

->`upload`: `O(log n)` if reusing an id, otherwise `O(1)`
->`remove`: `O(log n)`
->`watch`: `O(k)` where `k` is returned substring length
->`like`, `dislike`, `getLikesAndDislikes`, `getViews`: `O(1)`

## Idea

We need to support two things efficiently:

1. **Store video data and counters by `videoId`**

   ->video string
   ->likes
   ->dislikes
   ->views

2. **Always assign the smallest available `videoId`**

   ->If some ids were deleted, reuse the smallest one first
   ->This is exactly what a **min-heap*->is good for

So we maintain:

->`videos`: dictionary `{videoId: [video, likes, dislikes, views]}`
->`available`: min-heap of deleted ids ready to reuse
->`next_id`: the next new id if no reusable id exists
"""

import heapq
from typing import List


class VideoSharingPlatform:

    def __init__(self):
        self.videos = {}          # videoId -> [video_str, likes, dislikes, views]
        self.available = []       # min-heap of reusable ids
        self.next_id = 0

    def upload(self, video: str) -> int:
        if self.available:
            video_id = heapq.heappop(self.available)
        else:
            video_id = self.next_id
            self.next_id += 1

        self.videos[video_id] = [video, 0, 0, 0]
        return video_id

    def remove(self, video_id: int) -> None:
        if video_id in self.videos:
            del self.videos[video_id]
            heapq.heappush(self.available, video_id)

    def watch(self, video_id: int, start_minute: int, end_minute: int) -> str:
        if video_id not in self.videos:
            return "-1"

        video, likes, dislikes, views = self.videos[video_id]
        self.videos[video_id][3] += 1

        end = min(end_minute, len(video) - 1)
        return video[start_minute:end + 1]

    def like(self, video_id: int) -> None:
        if video_id in self.videos:
            self.videos[video_id][1] += 1

    def dislike(self, video_id: int) -> None:
        if video_id in self.videos:
            self.videos[video_id][2] += 1

    def get_likes_and_dislikes(self, video_id: int) -> List[int]:
        if video_id not in self.videos:
            return [-1]

        return [self.videos[video_id][1], self.videos[video_id][2]]

    def get_views(self, video_id: int) -> int:
        if video_id not in self.videos:
            return -1

        return self.videos[video_id][3]


# Complexity Analysis
"""
Let `n` be the number of active/deleted ids stored.

->`upload`: `O(log n)` in worst case due to heap pop
->`remove`: `O(log n)` due to heap push
->`watch`: `O(k)` where `k` is substring length returned
->`like`: `O(1)`
->`dislike`: `O(1)`
->`getLikesAndDislikes`: `O(1)`
->`getViews`: `O(1)`

# Space

->`O(total uploaded video length + number of ids)`
"""