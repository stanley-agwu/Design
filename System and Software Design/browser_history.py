# Design Browser History

"""
You have a browser of one tab where you start on the homepage and you can visit another url, get back in the history number of steps or move forward in the history number of steps.

Implement the BrowserHistory class:

BrowserHistory(string homepage) Initializes the object with the homepage of the browser.
void visit(string url) Visits url from the current page. It clears up all the forward history.
string back(int steps) Move steps back in history. If you can only return x steps in the history and steps > x, you will return only x steps. Return the current url after moving back in history at most steps.
string forward(int steps) Move steps forward in history. If you can only forward x steps in the history and steps > x, you will forward only x steps. Return the current url after forwarding in history at most steps.
 

Example:

Input:
["BrowserHistory","visit","visit","visit","back","back","forward","visit","forward","back","back"]
[["leetcode.com"],["google.com"],["facebook.com"],["youtube.com"],[1],[1],[1],["linkedin.com"],[2],[2],[7]]
Output:
[null,null,null,null,"facebook.com","google.com","facebook.com",null,"linkedin.com","google.com","leetcode.com"]

Explanation:
BrowserHistory browserHistory = new BrowserHistory("leetcode.com");
browserHistory.visit("google.com");       // You are in "leetcode.com". Visit "google.com"
browserHistory.visit("facebook.com");     // You are in "google.com". Visit "facebook.com"
browserHistory.visit("youtube.com");      // You are in "facebook.com". Visit "youtube.com"
browserHistory.back(1);                   // You are in "youtube.com", move back to "facebook.com" return "facebook.com"
browserHistory.back(1);                   // You are in "facebook.com", move back to "google.com" return "google.com"
browserHistory.forward(1);                // You are in "google.com", move forward to "facebook.com" return "facebook.com"
browserHistory.visit("linkedin.com");     // You are in "facebook.com". Visit "linkedin.com"
browserHistory.forward(2);                // You are in "linkedin.com", you cannot move forward any steps.
browserHistory.back(2);                   // You are in "linkedin.com", move back two steps to "facebook.com" then to "google.com". return "google.com"
browserHistory.back(7);                   // You are in "google.com", you can move back only one step to "leetcode.com". return "leetcode.com"
 

Constraints:

1 <= homepage.length <= 20
1 <= url.length <= 20
1 <= steps <= 100
homepage and url consist of  '.' or lower case English letters.
At most 5000 calls will be made to visit, back, and forward.
"""

class BrowserHistory:

    def __init__(self, homepage: str):
        self.history = [homepage]
        self.curr = 0
        self.last = 0

    def visit(self, url: str) -> None:
        self.curr += 1

        if self.curr == len(self.history):
            self.history.append(url)
        else:
            self.history[self.curr] = url

        self.last = self.curr

    def back(self, steps: int) -> str:
        self.curr = max(0, self.curr - steps)
        return self.history[self.curr]

    def forward(self, steps: int) -> str:
        self.curr = min(self.last, self.curr + steps)
        return self.history[self.curr]
    
# Complexity Analysis
"""
Time Complexity: O(1) for each method call.
Space Complexity: O(N) where N is the number of urls visited. In the worst case, we could visit 5000 urls, so the space complexity is O(5000) = O(1) in terms of big O notation.
"""


# Alternative Solution - Using Two stacks

class BrowserHistory:

    def __init__(self, homepage: str):
        self.curr = homepage
        self.back_stack = []
        self.forward_stack = []

    def visit(self, url: str) -> None:
        self.back_stack.append(self.curr)
        self.curr = url
        self.forward_stack.clear()

    def back(self, steps: int) -> str:
        while steps > 0 and self.back_stack:
            self.forward_stack.append(self.curr)
            self.curr = self.back_stack.pop()
            steps -= 1
        return self.curr

    def forward(self, steps: int) -> str:
        while steps > 0 and self.forward_stack:
            self.back_stack.append(self.curr)
            self.curr = self.forward_stack.pop()
            steps -= 1
        return self.curr
    
# Complexity Analysis
"""
Time Complexity: O(1) for each method call.
Space Complexity: O(N) where N is the number of urls visited. In the worst case, we could visit 5000 urls, so the space complexity is O(5000) = O(1) in terms of big O notation.
"""
