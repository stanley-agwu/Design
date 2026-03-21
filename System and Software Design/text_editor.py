# Design a Text Editor

# Tag -> Hard

"""
Design a text editor with a cursor that can do the following:

Add text to where the cursor is.
Delete text from where the cursor is (simulating the backspace key).
Move the cursor either left or right.
When deleting text, only characters to the left of the cursor will be deleted. 
The cursor will also remain within the actual text and cannot be moved beyond 
it. More formally, we have that 0 <= cursor.position <= currentText.length 
always holds.

Implement the TextEditor class:

TextEditor() Initializes the object with empty text.
void addText(string text) Appends text to where the cursor is. The cursor ends 
    to the right of text.
int deleteText(int k) Deletes k characters to the left of the cursor. Returns 
    the number of characters actually deleted.
string cursorLeft(int k) Moves the cursor to the left k times. Returns the 
    last min(10, len) characters to the left of the cursor, where len is the 
    number of characters to the left of the cursor.
string cursorRight(int k) Moves the cursor to the right k times. Returns the 
    last min(10, len) characters to the left of the cursor, where len is the 
    number of characters to the left of the cursor.
 
Example 1:

Input
["TextEditor", "addText", "deleteText", "addText", "cursorRight", "cursorLeft", 
    "deleteText", "cursorLeft", "cursorRight"]
[[], ["leetcode"], [4], ["practice"], [3], [8], [10], [2], [6]]
Output
[null, null, 4, null, "etpractice", "leet", 4, "", "practi"]

Explanation
TextEditor textEditor = new TextEditor(); // The current text is "|". 
    (The '|' character represents the cursor)
textEditor.addText("leetcode"); // The current text is "leetcode|".
textEditor.deleteText(4); // return 4
                          // The current text is "leet|". 
                          // 4 characters were deleted.
textEditor.addText("practice"); // The current text is "leetpractice|". 
textEditor.cursorRight(3); // return "etpractice"
                           // The current text is "leetpractice|". 
                           // The cursor cannot be moved beyond the actual text 
                           and thus did not move.
                           // "etpractice" is the last 10 characters to the left of the cursor.
textEditor.cursorLeft(8); // return "leet"
                          // The current text is "leet|practice".
                          // "leet" is the last min(10, 4) = 4 characters to the left of the cursor.
textEditor.deleteText(10); // return 4
                           // The current text is "|practice".
                           // Only 4 characters were deleted.
textEditor.cursorLeft(2); // return ""
                          // The current text is "|practice".
                          // The cursor cannot be moved beyond the actual text and thus did not move. 
                          // "" is the last min(10, 0) = 0 characters to the left of the cursor.
textEditor.cursorRight(6); // return "practi"
                           // The current text is "practi|ce".
                           // "practi" is the last min(10, 6) = 6 characters to the left of the cursor.
 

Constraints:

1 <= text.length, k <= 40
text consists of lowercase English letters.
At most 2 * 104 calls in total will be made to addText, deleteText, 
    cursorLeft and cursorRight.

Follow-up: Could you find a solution with time complexity of O(k) per call?
"""

# Idea
"""
Use two stacks (or two dynamic arrays / lists):

-> left: characters to the left of the cursor
-> right: characters to the right of the cursor

This is the standard way to simulate a text editor cursor efficiently.
When the cursor moves:
-> left: pop from left, push to right
-> right: pop from right, push to left

When adding text:
-> append all characters to left

When deleting text:
-> pop from left

This gives O(k) per operation, which matches the follow-up.
"""

class TextEditor:

    def __init__(self):
        self.left = []
        self.right = []

    def add_text(self, text: str) -> None:
        for ch in text:
            self.left.append(ch)

    def delete_text(self, k: int) -> int:
        deleted = min(k, len(self.left))
        for _ in range(deleted):
            self.left.pop()
        return deleted

    def cursor_left(self, k: int) -> str:
        moves = min(k, len(self.left))
        for _ in range(moves):
            self.right.append(self.left.pop())
        return "".join(self.left[-10:])

    def cursor_right(self, k: int) -> str:
        moves = min(k, len(self.right))
        for _ in range(moves):
            self.left.append(self.right.pop())
        return "".join(self.left[-10:])


# Complexity analysis
"""
Let k be the parameter in each operation.
-> add_text(text): O(len(text))
-> delete_text(k): O(k)
-> cursor_left(k): O(k)
-> cursor_right(k): O(k)

Returning the last 10 characters costs only O(10), which is constant.

Space complexity: O(n), where n is total text size.
"""
