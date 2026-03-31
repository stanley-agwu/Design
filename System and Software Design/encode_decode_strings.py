# Encode and Decode Strings

"""
Design an algorithm to encode a list of strings to a string. The encoded string 
is then sent over the network and is decoded back to the original list of strings.

Machine 1 (sender) has the function:

string encode(vector<string> strs) {
  // ... your code
  return encoded_string;
}
Machine 2 (receiver) has the function:
vector<string> decode(string s) {
  //... your code
  return strs;
}
So Machine 1 does:

string encoded_string = encode(strs);
and Machine 2 does:

vector<string> strs2 = decode(encoded_string);
strs2 in Machine 2 should be the same as strs in Machine 1.

Implement the encode and decode methods.

You are not allowed to solve the problem using any serialize methods (such as eval).

Example 1:

Input: dummy_input = ["Hello","World"]
Output: ["Hello","World"]
Explanation:
Machine 1:
Codec encoder = new Codec();
String msg = encoder.encode(strs);
Machine 1 ---msg---> Machine 2

Machine 2:
Codec decoder = new Codec();
String[] strs = decoder.decode(msg);
Example 2:

Input: dummy_input = [""]
Output: [""]

Constraints:

1 <= strs.length <= 200
0 <= strs[i].length <= 200
strs[i] contains any possible characters out of 256 valid ASCII characters.
 

Follow up: Could you write a generalized algorithm to work on any possible set 
of characters?
"""

class Codec:
    def encode(self, strs: list[str]) -> str:
        """
        Encodes a list of strings into a single string.

        Format for each string:
            <length>#<string>

        Example:
            ["Hello", "World"] -> "5#Hello5#World"
        """
        encoded_parts = []

        for s in strs:
            encoded_parts.append(str(len(s)))
            encoded_parts.append('#')
            encoded_parts.append(s)

        return ''.join(encoded_parts)

    def decode(self, s: str) -> list[str]:
        """
        Decodes a single encoded string back into the original list of strings.
        """
        result = []
        idx = 0
        n = len(s)

        while idx < n:
            # Find the separator '#'
            left = idx
            while s[left] != '#':
                left += 1

            # Length is the substring before '#'
            length = int(s[idx:left])

            # Extract the actual string of that length
            start = left + 1
            end = start + length
            result.append(s[start:end])

            # Move to the next encoded block
            idx = end

        return result
    
# Complexity Analysis
"""
Let n be the total length of all strings in the input list.
encode: O(n) time to construct the encoded string, O(n) space for the output 
    string.
decode: O(n) time to parse the encoded string, O(m) space for the output list 
    of strings, where m is the number of strings.
"""
