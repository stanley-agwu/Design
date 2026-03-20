# Booking Concert Tickets in Groups

"""
A concert hall has n rows numbered from 0 to n - 1, each with m seats, 
numbered from 0 to m - 1. You need to design a ticketing system that can 
allocate seats in the following cases:

If a group of k spectators can sit together in a row.
If every member of a group of k spectators can get a seat. They may or may 
not sit together.
Note that the spectators are very picky. Hence:

They will book seats only if each member of their group can get a seat with 
row number less than or equal to maxRow. maxRow can vary from group to group.
In case there are multiple rows to choose from, the row with the smallest 
number is chosen. If there are multiple seats to choose in the same row, the seat with the smallest number is chosen.
Implement the BookMyShow class:

BookMyShow(int n, int m) Initializes the object with n as number of rows and 
    m as number of seats per row.
int[] gather(int k, int maxRow) Returns an array of length 2 denoting the 
    row and seat number (respectively) of the first seat being allocated 
    to the k members of the group, who must sit together. In other words, 
    it returns the smallest possible r and c such that all [c, c + k - 1] 
    seats are valid and empty in row r, and r <= maxRow. Returns [] in case 
    it is not possible to allocate seats to the group.
boolean scatter(int k, int maxRow) Returns true if all k members of the 
    group can be allocated seats in rows 0 to maxRow, who may or may not 
    sit together. If the seats can be allocated, it allocates k seats to the 
    group with the smallest row numbers, and the smallest possible seat 
    numbers in each row. Otherwise, returns false.
 
Example 1:

Input
["BookMyShow", "gather", "gather", "scatter", "scatter"]
[[2, 5], [4, 0], [2, 0], [5, 1], [5, 1]]
Output
[null, [0, 0], [], true, false]

Explanation
BookMyShow bms = new BookMyShow(2, 5); // There are 2 rows with 5 seats each 
bms.gather(4, 0); // return [0, 0]
                  // The group books seats [0, 3] of row 0. 
bms.gather(2, 0); // return []
                  // There is only 1 seat left in row 0,
                  // so it is not possible to book 2 consecutive seats. 
bms.scatter(5, 1); // return True
                   // The group books seat 4 of row 0 and seats [0, 3] of row 1. 
bms.scatter(5, 1); // return False
                   // There is only one seat left in the hall.
 

Constraints:

1 <= n <= 5 * 104
1 <= m, k <= 109
0 <= maxRow <= n - 1
At most 5 * 104 calls in total will be made to gather and scatter.
"""

# Idea
# Use a segment tree.

## Key observation
"""
Because of the booking rules, seats in every row are always filled **from left to right**.

That means for each row, we do **not** need to track every seat individually.
We only need to know:

* how many seats are already used in that row, or equivalently
* how many seats remain in that row

If a row has `remain[r]` seats left, then:

* `gather(k, max_row)` needs the **smallest row `r <= max_row`** with `remain[r] >= k`
* `scatter(k, max_row)` needs to know whether the **total remaining seats** in rows `[0..max_row]` is at least `k`

So we need a data structure that supports:

* point update on one row
* range maximum query
* range sum query
* find the first row whose remaining seats are at least `k`

A segment tree handles all of these efficiently.

---

# Data structure design

For every segment tree node, store:

* `mx`: maximum remaining seats in that segment
* `sm`: total remaining seats in that segment

Also keep:

* `used[r]`: how many seats are already occupied in row `r`
* `ptr`: first row that is not yet completely full, used by `scatter`

Initially:

* every row has `m` seats remaining
* `used[r] = 0`

---

# Operations

## 1. `gather(k, max_row)`

We need the smallest row `r <= max_row` with `remain[r] >= k`.

Using the segment tree:

* first check whether the maximum remaining seats in rows `[0..max_row]` is at least `k`
* if not, return `[]`
* otherwise, descend the tree to find the leftmost such row

Once found:

* answer is `[r, used[r]]`
* update `used[r] += k`
* update segment tree at row `r`

---

## 2. `scatter(k, max_row)`

We need enough total seats in rows `[0..max_row]`.

Using the segment tree:

* query sum of remaining seats in `[0..max_row]`
* if sum < `k`, return `False`

Otherwise allocate greedily from the smallest row numbers:

* start from `ptr`
* while `k > 0`:

  * if row `ptr` is full, move `ptr += 1`
  * otherwise take as many seats as possible from that row
  * update the row in segment tree
  * if the row becomes full, move `ptr += 1`

This is efficient because `ptr` only moves forward, and each row becomes full at most once.

---

# Complexity

Let `n` be number of rows.

## Time

* `gather`: `O(log n)`
* `scatter`:

  * sum check: `O(log n)`
  * each touched row update: `O(log n)`
  * across all operations, rows are advanced at most `n` times

So total complexity over all calls is efficient enough for the constraints.

## Space

* `O(n)` for segment tree and row state
"""

class SegmentTree:
    def __init__(self, n: int, m: int):
        self.n = n
        self.mx = [0] * (4 * n)
        self.sm = [0] * (4 * n)
        self._build(1, 0, n - 1, m)

    def _build(self, idx: int, left: int, right: int, m: int) -> None:
        if left == right:
            self.mx[idx] = m
            self.sm[idx] = m
            return

        mid = (left + right) // 2
        self._build(idx * 2, left, mid, m)
        self._build(idx * 2 + 1, mid + 1, right, m)
        self._pull(idx)

    def _pull(self, idx: int) -> None:
        self.mx[idx] = max(self.mx[idx * 2], self.mx[idx * 2 + 1])
        self.sm[idx] = self.sm[idx * 2] + self.sm[idx * 2 + 1]

    def update(self, pos: int, val: int, idx: int = 1, left: int = 0, right: int = None) -> None:
        if right is None:
            right = self.n - 1

        if left == right:
            self.mx[idx] = val
            self.sm[idx] = val
            return

        mid = (left + right) // 2
        if pos <= mid:
            self.update(pos, val, idx * 2, left, mid)
        else:
            self.update(pos, val, idx * 2 + 1, mid + 1, right)

        self._pull(idx)

    def query_sum(self, ql: int, qr: int, idx: int = 1, left: int = 0, right: int = None) -> int:
        if right is None:
            right = self.n - 1

        if ql <= left and right <= qr:
            return self.sm[idx]
        if right < ql or qr < left:
            return 0

        mid = (left + right) // 2
        return self.query_sum(ql, qr, idx * 2, left, mid) + \
               self.query_sum(ql, qr, idx * 2 + 1, mid + 1, right)

    def query_max(self, ql: int, qr: int, idx: int = 1, left: int = 0, right: int = None) -> int:
        if right is None:
            right = self.n - 1

        if ql <= left and right <= qr:
            return self.mx[idx]
        if right < ql or qr < left:
            return 0

        mid = (left + right) // 2
        return max(
            self.query_max(ql, qr, idx * 2, left, mid),
            self.query_max(ql, qr, idx * 2 + 1, mid + 1, right)
        )

    def first_row_with_at_least(self, ql: int, qr: int, k: int, idx: int = 1, left: int = 0, right: int = None) -> int:
        if right is None:
            right = self.n - 1

        if right < ql or qr < left or self.mx[idx] < k:
            return -1

        if left == right:
            return left

        mid = (left + right) // 2
        res = self.first_row_with_at_least(ql, qr, k, idx * 2, left, mid)
        if res != -1:
            return res
        return self.first_row_with_at_least(ql, qr, k, idx * 2 + 1, mid + 1, right)


class BookMyShow:

    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.used = [0] * n
        self.seg = SegmentTree(n, m)
        self.ptr = 0  # first row that is not completely full

    def gather(self, k: int, max_row: int) -> list[int]:
        if self.seg.query_max(0, max_row) < k:
            return []

        row = self.seg.first_row_with_at_least(0, max_row, k)
        seat = self.used[row]

        self.used[row] += k
        remain = self.m - self.used[row]
        self.seg.update(row, remain)

        return [row, seat]

    def scatter(self, k: int, max_row: int) -> bool:
        if self.seg.query_sum(0, max_row) < k:
            return False

        while k > 0:
            while self.ptr <= max_row and self.used[self.ptr] == self.m:
                self.ptr += 1

            take = min(k, self.m - self.used[self.ptr])
            self.used[self.ptr] += take
            k -= take

            remain = self.m - self.used[self.ptr]
            self.seg.update(self.ptr, remain)

            if self.used[self.ptr] == self.m:
                self.ptr += 1

        return True


