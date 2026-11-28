# M3 Recursion, Backtracking & Bits: Student Handbook

Nov 27, 2026 · @Anoop

This module teaches you to search through every possibility efficiently, to use integers as sets, and ends with Contest 1.

## Lecture 9: Recursion, backtracking & meet in the middle

Backtracking tries every option, but gives up on a branch the moment it can't lead to an answer.

### 1. Size the search before you code

| What you generate | Count | Safe up to about |
| --- | --- | --- |
| All subsets of n items | 2^n | n = 20–22 |
| All permutations of n items | n! | n = 9–10 |
| Subsets via meet in the middle | 2 × 2^(n/2) | n = 40 |

### 2. The backtracking template

```text
solve(state):
    if state is complete: record it; return
    for each choice c that is still valid:
        apply c          # choose
        solve(state)     # recurse
        undo c           # un-choose
```

The “undo” step is what most bugs forget.

### 3. Worked example: Subsets

[LeetCode 78](https://leetcode.com/problems/subsets/). For each element, either leave it out or put it in.

```cpp
vector<vector<int>> res; vector<int> cur;
void go(const vector<int>& a, int i) {
    if (i == (int)a.size()) { res.push_back(cur); return; }
    go(a, i + 1);                                   // leave a[i] out
    cur.push_back(a[i]); go(a, i + 1); cur.pop_back();   // put it in, then undo
}
```

```java
List<List<Integer>> res = new ArrayList<>();
List<Integer> cur = new ArrayList<>();
void go(int[] a, int i) {
    if (i == a.length) { res.add(new ArrayList<>(cur)); return; }
    go(a, i + 1);
    cur.add(a[i]); go(a, i + 1); cur.remove(cur.size() - 1);
}
```

The same subsets with a loop: for mask from 0 to 2^n − 1, item i is in the subset when bit i of mask is 1 (Lecture 10).

### 4. Worked example: Creating Strings

[CSES 1622](https://cses.fi/problemset/task/1622). Print every distinct rearrangement of a string (length ≤ 8) in alphabetical order.

Sort the string first. In C++, `next_permutation` steps to the next arrangement in order and skips duplicates for you. In Java, backtrack over letter counts: at each position try each letter that still has copies left.

```cpp
string s; cin >> s; sort(s.begin(), s.end());
vector<string> out;
do out.push_back(s); while (next_permutation(s.begin(), s.end()));
cout << out.size() << '\n';
for (auto& t : out) cout << t << '\n';
```

```java
static int[] cnt = new int[26];
static StringBuilder all = new StringBuilder(); static int total = 0;
static void build(char[] cur, int pos) {
    if (pos == cur.length) { all.append(cur).append('\n'); total++; return; }
    for (int c = 0; c < 26; c++) if (cnt[c] > 0) {
        cnt[c]--; cur[pos] = (char) ('a' + c);
        build(cur, pos + 1);
        cnt[c]++;                                   // undo
    }
}
// main: count letters into cnt, call build(new char[n], 0), print total then all
```

### 5. Worked example: Chessboard and Queens

[CSES 1624](https://cses.fi/problemset/task/1624). Place 8 queens on an 8 × 8 board with some squares reserved, so no two attack each other. Count the ways.

Put one queen per row. Square (r, c) lies on diagonal r + c and anti-diagonal r − c + 7. Three boolean arrays tell you instantly whether a column or diagonal is taken.

```cpp
string b[8]; bool col[8], d1[15], d2[15]; int ways = 0;
void place(int r) {
    if (r == 8) { ways++; return; }
    for (int c = 0; c < 8; c++) {
        if (b[r][c] == '*' || col[c] || d1[r + c] || d2[r - c + 7]) continue;
        col[c] = d1[r + c] = d2[r - c + 7] = true;
        place(r + 1);
        col[c] = d1[r + c] = d2[r - c + 7] = false;
    }
}
```

```java
static char[][] b = new char[8][]; static boolean[] col = new boolean[8], d1 = new boolean[15], d2 = new boolean[15];
static int ways = 0;
static void place(int r) {
    if (r == 8) { ways++; return; }
    for (int c = 0; c < 8; c++) {
        if (b[r][c] == '*' || col[c] || d1[r + c] || d2[r - c + 7]) continue;
        col[c] = d1[r + c] = d2[r - c + 7] = true;
        place(r + 1);
        col[c] = d1[r + c] = d2[r - c + 7] = false;
    }
}
```

On an empty board the answer is 92.

### 6. Meet in the middle

Count subsets of n ≤ 40 numbers that sum to x ([CSES 1628](https://cses.fi/problemset/task/1628)). 2^40 ≈ 10^12 is too many. Instead:

1. Split the numbers into two halves of at most 20.
2. List all 2^20 subset sums of each half.
3. Sort the second list.
4. For each sum s in the first list, count how many sums in the second equal x − s (upper bound minus lower bound).

About 2^20 × 20 steps: fast.

### 7. Common mistakes

- Forgetting to undo a choice
- Copying the current list at every step instead of only at complete answers
- Recursion so deep it overflows the stack
- Java: storing 2^20 sums as `Long` objects. Use `long[]`

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Creating Strings](https://cses.fi/problemset/task/1622) | In-class | Easy | Worked above |
| [Chessboard and Queens](https://cses.fi/problemset/task/1624) | In-class | Medium | Worked above |
| [Subsets](https://leetcode.com/problems/subsets/) | In-class | Medium | Worked above |
| [Permutations](https://leetcode.com/problems/permutations/) | Take-home | Medium | Swap a\[i\] with each later element, recurse, swap back |
| [Combination Sum](https://leetcode.com/problems/combination-sum/) | Take-home | Medium | Pass a start index so you never go backwards |
| [Apple Division](https://cses.fi/problemset/task/1623) | Take-home | Easy | n ≤ 20: try every split |
| [Meet in the Middle](https://cses.fi/problemset/task/1628) | Take-home | Hard | Section 6 |
| [Word Search](https://leetcode.com/problems/word-search/) | Take-home | Medium | DFS from every cell; mark visited, unmark on return |

### Quiz

1. What are the three steps of every backtracking routine?
2. How many subsets do 20 items have? Is listing them all fast enough?
3. Which number identifies the anti-diagonal of square (r, c) on an 8 × 8 board?
4. Why does meet in the middle make n = 40 possible?
5. How do you avoid printing the same arrangement twice in Creating Strings?

## Lecture 10: Bit manipulation

An integer is a row of bits. Treat it as a set of up to 64 yes/no flags, and many problems get shorter and faster.

### 1. The operators

| Operator | Meaning | 12 (1100) op 10 (1010) |
| --- | --- | --- |
| & | AND: 1 if both are 1 | 8 (1000) |
| \| | OR: 1 if either is 1 | 14 (1110) |
| ^ | XOR: 1 if they differ | 6 (0110) |
| \~ | NOT: flip every bit |  |
| << k | shift left: multiply by 2^k | 12 << 1 = 24 |
| >> k | shift right: divide by 2^k | 12 >> 2 = 3 |

### 2. The toolkit

| Task | Expression |
| --- | --- |
| Is bit i set? | (x >> i) & 1 |
| Set bit i | x \| (1 << i) |
| Clear bit i | x & \~(1 << i) |
| Toggle bit i | x ^ (1 << i) |
| Lowest set bit | x & (−x) |
| Remove lowest set bit | x & (x − 1) |
| Is x a power of two? | x > 0 and (x & (x − 1)) == 0 |
| Count set bits | C++ `__builtin_popcountll(x)` · Java `Long.bitCount(x)` |

**Brackets!** `x & 1 == 0` means `x & (1 == 0)`. Write `(x & 1) == 0`.

**Width!** `1 << 40` overflows a 32-bit int. Write `1LL << 40` (C++) or `1L << 40` (Java).

### 3. Masks as sets

Number the items 0..n−1. A mask with bit i set means item i is chosen.

- Union: a | b · intersection: a & b · is a inside b: (a & b) == a
- Every subset of n items: `for (mask = 0; mask < (1 << n); mask++)`
- Every submask of m: `for (s = m; s > 0; s = (s - 1) & m)`

### 4. Worked example: Petr and a Combination Lock

[Codeforces 1097B](https://codeforces.com/problemset/problem/1097/B). Rotate the lock n ≤ 15 times by a\_i degrees, each either clockwise or counter-clockwise. Can it end at 0?

Each mask is one choice of directions: bit i = 1 means +a\_i, 0 means −a\_i. 2^15 = 32,768 masks.

```cpp
bool ok = false;
for (int m = 0; m < (1 << n); m++) {
    int s = 0;
    for (int i = 0; i < n; i++) s += ((m >> i) & 1) ? a[i] : -a[i];
    if (s % 360 == 0) ok = true;
}
cout << (ok ? "YES" : "NO") << '\n';
```

```java
boolean ok = false;
for (int m = 0; m < (1 << n); m++) {
    int s = 0;
    for (int i = 0; i < n; i++) s += ((m >> i) & 1) == 1 ? a[i] : -a[i];
    if (s % 360 == 0) ok = true;
}
out.println(ok ? "YES" : "NO");
```

### 5. XOR tricks

- x ^ x = 0 and x ^ 0 = x, so equal values cancel.
- XOR of a range works like a prefix sum: xor(l..r) = px\[r\] ^ px\[l−1\].

**Worked example: Single Number III** ([LeetCode 260](https://leetcode.com/problems/single-number-iii/)). Every number appears twice except two, a and b.

1. XOR everything: the pairs cancel, leaving x = a ^ b (not 0, because a ≠ b).
2. Pick a bit where a and b differ: the lowest set bit of x.
3. Split all numbers by that bit and XOR each group. One group gives a, the other b.

```cpp
vector<int> singleNumber(vector<int>& nums) {
    long long x = 0;
    for (int v : nums) x ^= v;
    long long low = x & -x;
    int a = 0, b = 0;
    for (int v : nums) (v & low) ? a ^= v : b ^= v;
    return {a, b};
}
```

```java
public int[] singleNumber(int[] nums) {
    int x = 0;
    for (int v : nums) x ^= v;
    int low = x & -x;                    // safe in Java: wraps without error
    int a = 0, b = 0;
    for (int v : nums) { if ((v & low) != 0) a ^= v; else b ^= v; }
    return new int[]{a, b};
}
```

### 6. Binary trie (idea for the take-home)

To find the maximum a ^ b in an array, insert each number's bits from the highest into a tree with two children per node (0 and 1). For each number, walk down preferring the opposite bit at each level: that greedily makes the highest bits of the XOR equal to 1. O(n × 31).

### 7. Common mistakes

- Missing brackets around bit operations
- 32-bit shifts for bits 31 and above
- Java: `>>` keeps the sign; use `>>>` for an unsigned shift

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Single Number III](https://leetcode.com/problems/single-number-iii/) | In-class | Medium | Worked above |
| [Petr and a Combination Lock](https://codeforces.com/problemset/problem/1097/B) | In-class | Easy | Worked above |
| [Counting Bits (LeetCode)](https://leetcode.com/problems/counting-bits/) | Take-home | Easy | bits(i) = bits(i / 2) + last bit of i |
| [Gray Code](https://cses.fi/problemset/task/2205) | Take-home | Medium | The i-th code is i ^ (i >> 1) |
| [Counting Bits (CSES)](https://cses.fi/problemset/task/1146) | Take-home | Hard | Count each bit position separately; bit b repeats in blocks of 2^(b+1) |
| [Maximum XOR of Two Numbers](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/) | Take-home | Medium | Section 6 |
| [Maximum Xor Subarray](https://cses.fi/problemset/task/1655) | Take-home | Hard | Prefix XORs, then Section 6 on them (include 0) |

### Quiz

1. Write the expression for “is bit 3 of x set”.
2. What does x & (x − 1) do?
3. Why is `1 << 40` wrong in C++, and how do you fix it?
4. How many masks are there for n = 15? Is looping over all of them fast?
5. In Single Number III, why split the numbers by one set bit of a ^ b?

## Lecture 11: Contest 1 + Greedy II

The first two hours are a timed contest on Modules 0–3. Afterwards: the editorial, then a short lesson on greedy with heaps and medians.

### 1. Contest rules

- 2 hours, individual, 4 problems, ICPC scoring (problems solved, then time + 20-minute penalty per wrong submission)
- Allowed: the judge, your template, language documentation. Not allowed: AI tools, messaging, other people's code
- Counts toward the 30% contest component

### 2. Contest playbook

1. **Minutes 0–10:** read all four problems. Write one line per problem: the constraint and your first idea.
2. Solve in order of how sure you are, not in the listed order.
3. Before each submit: test n = 1, the largest values, all-negative input, and the samples.
4. Stuck for 20 minutes? Move on. Come back with fresh eyes.
5. Wrong answer? Check overflow first, then edge cases, then the idea.

### 3. After the contest: Kadane's algorithm

Maximum subarray sum ([CSES 1643](https://cses.fi/problemset/task/1643)) in one pass: the best subarray ending at i either extends the best one ending at i − 1 or starts fresh at i.

```cpp
long long cur = LLONG_MIN / 2, best = LLONG_MIN;
for (long long x : a) { cur = max(x, cur + x); best = max(best, cur); }
cout << best << '\n';
```

```java
long cur = Long.MIN_VALUE / 2, best = Long.MIN_VALUE;
for (long x : a) { cur = Math.max(x, cur + x); best = Math.max(best, cur); }
out.println(best);
```

Trap: starting best at 0 gives the wrong answer when every number is negative.

### 4. Greedy II: a heap of “when does it free up”

**Room Allocation** ([CSES 1164](https://cses.fi/problemset/task/1164)). Customers arrive and leave; give each a room, reusing rooms, using as few as possible.

1. Sort customers by arrival.
2. Keep a min-heap of (departure day, room number) for occupied rooms.
3. For each customer: if the earliest departure is before their arrival, reuse that room; otherwise open a new room.

```cpp
sort(order.begin(), order.end(), [&](int i, int j){ return arr[i] < arr[j]; });
priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;   // {departure, room}
vector<int> room(n); int rooms = 0;
for (int i : order) {
    if (!pq.empty() && pq.top().first < arr[i]) { room[i] = pq.top().second; pq.pop(); }
    else room[i] = ++rooms;
    pq.push({dep[i], room[i]});
}
```

```java
Integer[] order = new Integer[n];
for (int i = 0; i < n; i++) order[i] = i;
Arrays.sort(order, (i, j) -> Integer.compare(arr[i], arr[j]));
PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> Integer.compare(x[0], y[0]));   // {departure, room}
int[] room = new int[n]; int rooms = 0;
for (int i : order) {
    if (!pq.isEmpty() && pq.peek()[0] < arr[i]) room[i] = pq.poll()[1];
    else room[i] = ++rooms;
    pq.add(new int[]{dep[i], room[i]});
}
```

### 5. Greedy II: the median trick

The sum of distances Σ |x\_i − c| is smallest when c is the **median** of the x\_i. [Stick Lengths](https://cses.fi/problemset/task/1074) is exactly this. [Arranging The Sheep](https://codeforces.com/problemset/problem/1520/E) becomes the same problem after replacing each sheep position p\_i (in sorted order) by p\_i − i.

### 6. Upsolve checklist (48 hours)

- [ ] Every contest problem you didn't solve is Accepted
- [ ] Each is marked “Upsolved” in the portal
- [ ] One line in your notebook: what the key idea was and why you missed it

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Subarray Sums I](https://cses.fi/problemset/task/1660) | Contest | Easy | Values are positive. Think of Lecture 4 |
| [Maximum Subarray Sum](https://cses.fi/problemset/task/1643) | Contest | Easy | Section 3 |
| [K-th Not Divisible by n](https://codeforces.com/problemset/problem/1352/C) | Contest | Easy | Each block of n numbers has n − 1 good ones |
| [Two Sets](https://cses.fi/problemset/task/1092) | Contest | Medium | Total must be even. Fill one set greedily from n downwards |
| [Room Allocation](https://cses.fi/problemset/task/1164) | Take-home | Medium | Section 4 |
| [Gas Station](https://leetcode.com/problems/gas-station/) | Take-home | Medium | If total gas ≥ total cost, start right after the lowest running balance |
| [Task Scheduler](https://leetcode.com/problems/task-scheduler/) | Take-home | Medium | The most frequent task decides the frame size |
| [Arranging The Sheep](https://codeforces.com/problemset/problem/1520/E) | Take-home | Medium | Section 5 |
| [Stick Lengths](https://cses.fi/problemset/task/1074) | Take-home | Easy | Section 5 |
