# Encode and Decode Tiny URL

"""
Note: This is a companion problem to the System Design problem: Design TinyURL.
TinyURL is a URL shortening service where you enter a URL such as 
https://leetcode.com/problems/design-tinyurl and it returns a short URL 
such as http://tinyurl.com/4e9iAk. Design a class to encode a URL and 
decode a tiny URL.

There is no restriction on how your encode/decode algorithm should work. 
You just need to ensure that a URL can be encoded to a tiny URL and the 
tiny URL can be decoded to the original URL.

Implement the Solution class:

Solution() Initializes the object of the system.
String encode(String longUrl) Returns a tiny URL for the given longUrl.
String decode(String shortUrl) Returns the original long URL for the given 
    shortUrl. It is guaranteed that the given shortUrl was encoded by the 
    same object.
 
Example 1:

Input: url = "https://leetcode.com/problems/design-tinyurl"
Output: "https://leetcode.com/problems/design-tinyurl"

Explanation:
Solution obj = new Solution();
string tiny = obj.encode(url); // returns the encoded tiny url.
string ans = obj.decode(tiny); // returns the original url after decoding it.
 

Constraints:

1 <= url.length <= 104
url is guranteed to be a valid URL.
"""

class Solution:
    def __init__(self):
        self.long_to_short = {}
        self.short_to_long = {}
        self.counter = 1
        self.base = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.prefix = "http://tinyurl.com/"

    def _to_base62(self, num: int) -> str:
        if num == 0:
            return self.base[0]

        chars = []
        while num > 0:
            chars.append(self.base[num % 62])
            num //= 62
        return "".join(reversed(chars))

    def encode(self, long_url: str) -> str:
        if long_url in self.long_to_short:
            return self.long_to_short[long_url]

        key = self._to_base62(self.counter)
        self.counter += 1

        short_url = self.prefix + key
        self.long_to_short[long_url] = short_url
        self.short_to_long[short_url] = long_url

        return short_url

    def decode(self, short_url: str) -> str:
        return self.short_to_long[short_url]
    
# Time complexity
"""
Let L be the URL length.

encode
- Hash map lookup/insert: O(1) average
- Base62 conversion: O(log n) where n is the counter, very small
Overall: O(L) dominated by handling the string

decode
- Hash map lookup: O(1) average
"""

# Space complexity
"""
If we encode N URLs, we store them in two hash maps:
O(N * average_url_length)
"""
