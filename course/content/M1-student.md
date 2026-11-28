# M1 Array Techniques: Student Handbook

Nov 27, 2026 · @Anoop

## Module at a glance

Four techniques turn most O(n^2) array problems into O(n) or O(n log n). Learn the trigger words for each.

| Technique | Lecture | Use it when the problem says… | Cost |
| --- | --- | --- | --- |
| Prefix sums | L3 | “sum of range l..r”, many queries, many range updates | O(n) build, O(1) per query |
| Two pointers / sliding window | L4 | “longest/shortest contiguous subarray such that…”, sorted pair sums | O(n) |
| Hashing + prefix sums | L5 | “count subarrays with sum k”, “count pairs with…”, negatives allowed | O(n) average |
| Greedy with sorting | L6 | “maximum number of non-overlapping…”, “minimum rooms/rides/arrows” | O(n log n) |

## Lecture 3: Prefix sums & difference arrays

Precompute running totals once, and every range sum becomes one subtraction.

### 1. 1D prefix sums

Define p\[0\] = 0 and p\[i\] = a\[1\] + … + a\[i\]. Then

```latex
\text{sum}(l..r) = p[r] - p[l-1]
```

**Dry run.** a = \[3, 1, 4, 1, 5\] gives p = \[0, 3, 4, 8, 9, 14\]. sum(2..4) = p\[4\] − p\[1\] = 9 − 3 = 6, and 1 + 4 + 1 = 6. Correct.

Why p\[0\] = 0? It makes the formula work for l = 1 without a special case.

### 2. Worked example: Static Range Sum Queries

[CSES 1646](https://cses.fi/problemset/task/1646). n, q ≤ 2 × 10^5. Answering each query with a loop is up to 4 × 10^10 steps, far too slow. With prefix sums it is O(n + q).

```cpp
int n, q; cin >> n >> q;
vector<long long> p(n + 1, 0);
for (int i = 1; i <= n; i++) { long long x; cin >> x; p[i] = p[i-1] + x; }
while (q--) {
    int a, b; cin >> a >> b;
    cout << p[b] - p[a-1] << '\n';
}
```

```java
int n = nextInt(), q = nextInt();
long[] p = new long[n + 1];
for (int i = 1; i <= n; i++) p[i] = p[i - 1] + nextLong();
while (q-- > 0) {
    int a = nextInt(), b = nextInt();
    out.println(p[b] - p[a - 1]);
}
```

### 3. 2D prefix sums

P\[i\]\[j\] = sum of the rectangle from (1,1) to (i,j). Build it with

```latex
P[i][j] = a[i][j] + P[i-1][j] + P[i][j-1] - P[i-1][j-1]
```

and answer a rectangle (y1, x1)–(y2, x2) with

```latex
P[y_2][x_2] - P[y_1-1][x_2] - P[y_2][x_1-1] + P[y_1-1][x_1-1]
```

The last term is added back because the top-left block was subtracted twice.

### 4. Worked example: Forest Queries

[CSES 1652](https://cses.fi/problemset/task/1652). An n × n grid (n ≤ 1000) of `.` and `*` (trees). Answer up to 2 × 10^5 “how many trees in this rectangle” queries.

```cpp
vector<vector<int>> P(n + 1, vector<int>(n + 1, 0));
for (int i = 1; i <= n; i++) {
    string row; cin >> row;
    for (int j = 1; j <= n; j++)
        P[i][j] = (row[j-1] == '*') + P[i-1][j] + P[i][j-1] - P[i-1][j-1];
}
while (q--) {
    int y1, x1, y2, x2; cin >> y1 >> x1 >> y2 >> x2;
    cout << P[y2][x2] - P[y1-1][x2] - P[y2][x1-1] + P[y1-1][x1-1] << '\n';
}
```

```java
int[][] P = new int[n + 1][n + 1];
for (int i = 1; i <= n; i++) {
    String row = br.readLine().trim();
    for (int j = 1; j <= n; j++)
        P[i][j] = (row.charAt(j - 1) == '*' ? 1 : 0) + P[i-1][j] + P[i][j-1] - P[i-1][j-1];
}
while (q-- > 0) {
    int y1 = nextInt(), x1 = nextInt(), y2 = nextInt(), x2 = nextInt();
    out.println(P[y2][x2] - P[y1-1][x2] - P[y2][x1-1] + P[y1-1][x1-1]);
}
```

### 5. Difference arrays: many range updates

To add v to every position in l..r, many times, then read the final array:

1. Keep d of size n + 2, all zeros.
2. For each update: d\[l\] += v and d\[r + 1\] −= v.
3. At the end, prefix-sum d. Position i holds the total added there.

**Dry run.** n = 6, updates +5 on \[2, 4\] and +3 on \[3, 6\]. d\[1..7\] = \[0, 5, 3, 0, −5, 0, −3\]. Prefix sums give 0, 5, 8, 8, 3, 3 for positions 1..6.

Each update costs O(1) instead of O(n).

### 6. Prefix and suffix aggregates

For operations you can't subtract (max, min, product with zeros), build arrays from both ends:

- pre\[i\] = best of a\[1..i\]
- suf\[i\] = best of a\[i..n\]

Then “best of everything except position i” is combine(pre\[i−1\], suf\[i+1\]). That is the key to Product of Array Except Self and Maximal Intersection.

### 7. Common mistakes

- A prefix array of size n instead of n + 1
- `int` sums when n × max value exceeds 2 × 10^9
- In 2D, forgetting to add back the top-left corner
- Forgetting d\[r + 1\] −= v, or making d too small for r + 1

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Static Range Sum Queries](https://cses.fi/problemset/task/1646) | In-class | Easy | Worked above |
| [Forest Queries](https://cses.fi/problemset/task/1652) | In-class | Easy | Worked above |
| [Number of Ways](https://codeforces.com/problemset/problem/466/C) | Take-home | Medium | Total must divide by 3. Count how many earlier prefixes hit one third |
| [Perform the Combo](https://codeforces.com/problemset/problem/1311/C) | Take-home | Easy | Each mistake replays a prefix. Count how often each prefix length is pressed |
| [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | Take-home | Medium | Product of everything left of i times everything right of i. No division |
| [Maximal Intersection](https://codeforces.com/problemset/problem/1029/C) | Take-home | Medium | Intersection = \[max left, min right\]. Remove one segment using prefix/suffix arrays |

### Quiz

1. With 1-indexed prefix p, write sum(l..r).
2. Why is the top-left corner added back in the 2D formula?
3. How do you add v to positions l..r with a difference array?
4. Can prefix sums answer “minimum of l..r”? Why or why not?
5. n = 2 × 10^5 and values up to 10^9. Which type holds the prefix sums?

## Lecture 4: Two pointers & sliding window

Two indices that only move forward can replace a double loop, turning O(n^2) into O(n).

### 1. When does it work?

Two pointers need a **monotone** condition. For a window \[l, r\]: if it is valid, every window inside it is also valid (or, for other problems, every window containing it is). Then you never need to move a pointer backwards.

- “Longest subarray with sum ≤ t” with **positive** numbers: monotone. Works.
- Same question with negative numbers: not monotone. Use prefix sums + hashing (Lecture 5).

### 2. Pattern A: opposite ends on a sorted array

Find two numbers summing to x in a sorted array. Start l at the left, r at the right.

- sum < x → move l right (need bigger)
- sum > x → move r left (need smaller)
- sum = x → found

Each step throws away one candidate for good, so it takes at most n steps.

### 3. Worked example: Sum of Two Values

[CSES 1640](https://cses.fi/problemset/task/1640). Print the **original** 1-based positions of two different values summing to x, or IMPOSSIBLE. Sort (value, index) pairs so you don't lose the positions.

```cpp
vector<pair<long long,int>> v(n);
for (int i = 0; i < n; i++) { cin >> v[i].first; v[i].second = i + 1; }
sort(v.begin(), v.end());
int l = 0, r = n - 1;
while (l < r) {
    long long s = v[l].first + v[r].first;
    if (s == x) { cout << v[l].second << ' ' << v[r].second << '\n'; return; }
    if (s < x) l++; else r--;
}
cout << "IMPOSSIBLE\n";
```

```java
long[][] v = new long[n][2];
for (int i = 0; i < n; i++) { v[i][0] = nextLong(); v[i][1] = i + 1; }
Arrays.sort(v, (p, q) -> Long.compare(p[0], q[0]));
int l = 0, r = n - 1;
while (l < r) {
    long s = v[l][0] + v[r][0];
    if (s == x) { out.println(v[l][1] + " " + v[r][1]); return; }
    if (s < x) l++; else r--;
}
out.println("IMPOSSIBLE");
```

### 4. Pattern B: the sliding window template

```text
l = 0
for r in 0..n-1:
    add a[r] to the window
    while the window is invalid:
        remove a[l] from the window; l = l + 1
    the window [l, r] is valid: update the answer
```

### 5. Worked example: Books

[Codeforces 279B](https://codeforces.com/problemset/problem/279/B). Book i takes a\_i ≥ 1 minutes. You have t minutes and read consecutive books from any start. Maximum number of books = longest window with sum ≤ t.

**Dry run.** a = \[3, 1, 2, 1\], t = 5.

| r | add | sum | shrink? | window | length |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | 3 | no | \[3\] | 1 |
| 1 | 1 | 4 | no | \[3,1\] | 2 |
| 2 | 2 | 6 | drop 3 → 3 | \[1,2\] | 2 |
| 3 | 1 | 4 | no | \[1,2,1\] | 3 |

Answer 3.

```cpp
long long sum = 0; int l = 0, best = 0;
for (int r = 0; r < n; r++) {
    sum += a[r];
    while (sum > t) sum -= a[l++];
    best = max(best, r - l + 1);
}
cout << best << '\n';
```

```java
long sum = 0; int l = 0, best = 0;
for (int r = 0; r < n; r++) {
    sum += a[r];
    while (sum > t) sum -= a[l++];
    best = Math.max(best, r - l + 1);
}
out.println(best);
```

### 6. Worked example: Longest Substring Without Repeating Characters

[LeetCode 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/). The window is invalid when some character appears twice.

```cpp
int lengthOfLongestSubstring(string s) {
    vector<int> cnt(256, 0);
    int l = 0, best = 0;
    for (int r = 0; r < (int)s.size(); r++) {
        cnt[(unsigned char)s[r]]++;
        while (cnt[(unsigned char)s[r]] > 1) cnt[(unsigned char)s[l++]]--;
        best = max(best, r - l + 1);
    }
    return best;
}
```

```java
public int lengthOfLongestSubstring(String s) {
    int[] cnt = new int[256];
    int l = 0, best = 0;
    for (int r = 0; r < s.length(); r++) {
        cnt[s.charAt(r)]++;
        while (cnt[s.charAt(r)] > 1) cnt[s.charAt(l++)]--;
        best = Math.max(best, r - l + 1);
    }
    return best;
}
```

### 7. Pattern C: fixed-size windows

For windows of exactly k items: add a\[r\], and once r ≥ k, remove a\[r − k\]. Every window is processed in O(1).

### 8. Common mistakes

- Shrinking with `if` instead of `while`
- Recording the answer before the window is valid again
- Using two pointers when values can be negative
- Losing original indices when you sort

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Sum of Two Values](https://cses.fi/problemset/task/1640) | In-class | Easy | Worked above |
| [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | In-class | Medium | Worked above |
| [Books](https://codeforces.com/problemset/problem/279/B) | In-class | Medium | Worked above |
| [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/) | Take-home | Hard | Count what you still need. Grow until satisfied, then shrink while still satisfied |
| [Sum of Three Values](https://cses.fi/problemset/task/1641) | Take-home | Medium | Fix the first value, then use Pattern A on the rest. n ≤ 5000 |
| [Ternary String](https://codeforces.com/problemset/problem/1354/B) | Take-home | Easy | Shortest window containing 1, 2 and 3 |
| [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) | Take-home | Medium | Start at both ends. Which side can never help if you keep it? |

### Quiz

1. Why is the sliding window O(n) even with a `while` inside a `for`?
2. What property must the window condition have?
3. Why does Books break with negative reading times?
4. In Container With Most Water, which pointer do you move, and why?
5. In Sum of Two Values, what must you store before sorting?

## Lecture 5: Hashing & frequency techniques

Ask “which earlier value would make the current position an answer?”, then look it up in a hash map in O(1).

### 1. Hash maps in one paragraph

A hash map stores key → value pairs in buckets chosen by a hash of the key. Lookups, inserts and updates are O(1) on average. In the worst case (many keys in one bucket) they degrade to O(n). Codeforces sometimes has tests built to cause this. The defences are in section 6.

### 2. The key identity

With prefix sums p, a subarray l..r has sum k exactly when

```latex
p[r] - p[l-1] = k \iff p[l-1] = p[r] - k
```

So at each r, the number of good subarrays ending at r equals **how many earlier prefixes equal p\[r\] − k**. Keep a map from prefix value to count.

### 3. Worked example: Subarray Sum Equals K

[LeetCode 560](https://leetcode.com/problems/subarray-sum-equals-k/), also [CSES 1661 Subarray Sums II](https://cses.fi/problemset/task/1661). Values may be negative, so two pointers don't work.

**Dry run.** a = \[1, 2, 3, −2, 2\], k = 3.

| i | a\[i\] | prefix p | look for p − 3 | found | running answer |
| --- | --- | --- | --- | --- | --- |
| start |  | 0 |  |  | 0 (map {0:1}) |
| 1 | 1 | 1 | −2 | 0 | 0 |
| 2 | 2 | 3 | 0 | 1 | 1 |
| 3 | 3 | 6 | 3 | 1 | 2 |
| 4 | −2 | 4 | 1 | 1 | 3 |
| 5 | 2 | 6 | 3 | 1 | 4 |

The four subarrays: \[1,2\], \[3\], \[2,3,−2\], \[3,−2,2\].

```cpp
long long countSubarrays(const vector<long long>& a, long long k) {
    unordered_map<long long, long long> cnt;
    cnt.reserve(1 << 19);
    cnt[0] = 1;                       // the empty prefix
    long long p = 0, ans = 0;
    for (long long x : a) {
        p += x;
        auto it = cnt.find(p - k);    // look up BEFORE inserting p
        if (it != cnt.end()) ans += it->second;
        cnt[p]++;
    }
    return ans;
}
```

```java
static long countSubarrays(long[] a, long k) {
    HashMap<Long, Integer> cnt = new HashMap<>();
    cnt.put(0L, 1);                   // the empty prefix
    long p = 0, ans = 0;
    for (long x : a) {
        p += x;
        ans += cnt.getOrDefault(p - k, 0);   // look up BEFORE inserting p
        cnt.merge(p, 1, Integer::sum);
    }
    return ans;
}
```

### 4. Counting equal pairs

If a key appears c times, it forms c(c − 1)/2 pairs. Or count as you go: when the key appears for the c-th time, add c − 1.

### 5. Value transforms

Rewrite the condition so each side depends on one index only.

- Pairs i < j with a\[j\] − a\[i\] = j − i ⇔ a\[i\] − i = a\[j\] − j. Count equal values of a\[i\] − i.
- Subarrays with sum divisible by n ⇔ two prefixes with the same remainder mod n.

**Negative remainders.** In C++ and Java, −7 % 3 is −1, not 2. Normalise with ((x % m) + m) % m.

### 6. Staying safe from anti-hash tests

- **C++:** give `unordered_map` a randomised hash.

```cpp
struct SplitMix {
    static uint64_t splitmix64(uint64_t x) {
        x += 0x9e3779b97f4a7c15ULL;
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9ULL;
        x = (x ^ (x >> 27)) * 0x94d049bb133111ebULL;
        return x ^ (x >> 31);
    }
    size_t operator()(uint64_t x) const {
        static const uint64_t R = chrono::steady_clock::now().time_since_epoch().count();
        return splitmix64(x + R);
    }
};
unordered_map<long long, int, SplitMix> safeMap;
```

- **Java:** XOR keys with a random salt before inserting, or use a `TreeMap` (O(log n), always safe).

### 7. Common mistakes

- Forgetting `cnt[0] = 1` before the loop
- Inserting the current prefix before looking up (counts empty subarrays when k = 0)
- `int` prefix sums that overflow
- C++: using `map[x]` to test existence. It inserts x with value 0. Use `find` or `count`

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Subarray Sums II](https://cses.fi/problemset/task/1661) | In-class | Medium | Worked above |
| [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | In-class | Medium | Worked above |
| [Subarray Divisibility](https://cses.fi/problemset/task/1662) | Take-home | Medium | Equal prefix remainders mod n. Normalise negatives |
| [Same Differences](https://codeforces.com/problemset/problem/1520/D) | Take-home | Easy | Transform to a\[i\] − i and count equal pairs. Use 64-bit |
| [Eugene and an array](https://codeforces.com/problemset/problem/1333/C) | Take-home | Hard | A subarray is good when all its prefix sums (including the one before it) are distinct |
| [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) | Take-home | Medium | Only start counting a run at x when x − 1 is missing |

### Quiz

1. Why do we insert prefix 0 before the scan?
2. Why don't two pointers work for Subarray Sums II?
3. What is ((−7 % 3) + 3) % 3?
4. A key appears 4 times. How many equal pairs does it form?
5. Name one defence against anti-hash tests.

## Lecture 6: Greedy I, sorting & intervals

A greedy algorithm makes the best-looking choice at each step and never looks back. It is fast and short, but only correct when you can prove it.

### 1. How to approach a greedy problem

1. Propose a rule (“always take the one that ends first”).
2. Try to break it on tiny inputs (2–4 items). Spend two minutes here.
3. If it survives, prove it with an **exchange argument**: take any optimal answer, swap its first choice for the greedy choice, and show it is still valid and no worse.
4. Only then code it.

### 2. Worked example: Movie Festival

[CSES 1629](https://cses.fi/problemset/task/1629). Watch as many whole movies as possible; no two can overlap.

| Rule | Breaks on | Result |
| --- | --- | --- |
| Shortest first | \[1,5\], \[4,7\], \[6,10\] | picks 1, best is 2 |
| Earliest start first | \[1,10\], \[2,3\], \[4,5\] | picks 1, best is 2 |
| **Earliest end first** | nothing | correct |

**Why earliest end works.** Let g end first among all movies. Any optimal schedule starts with some movie f that ends no earlier than g. Replace f by g: g ends even earlier, so it fits before everything else. Same count, still valid.

```cpp
vector<pair<int,int>> v(n);                     // {start, end}
for (auto& [s, e] : v) cin >> s >> e;
sort(v.begin(), v.end(), [](auto& x, auto& y){ return x.second < y.second; });
int cnt = 0, lastEnd = 0;
for (auto& [s, e] : v)
    if (s >= lastEnd) { cnt++; lastEnd = e; }
cout << cnt << '\n';
```

```java
int[][] v = new int[n][2];
for (int i = 0; i < n; i++) { v[i][0] = nextInt(); v[i][1] = nextInt(); }
Arrays.sort(v, (x, y) -> Integer.compare(x[1], y[1]));
int cnt = 0, lastEnd = 0;
for (int[] m : v)
    if (m[0] >= lastEnd) { cnt++; lastEnd = m[1]; }
out.println(cnt);
```

### 3. Sweep line: Restaurant Customers

[CSES 1619](https://cses.fi/problemset/task/1619). Find the maximum number of customers inside at the same time.

Turn each customer into two events: (arrival, +1) and (leaving, −1). Sort all 2n events by time and keep a running total. The answer is the largest total seen. O(n log n).

```cpp
vector<pair<int,int>> ev;
for (int i = 0; i < n; i++) { int a, b; cin >> a >> b; ev.push_back({a, +1}); ev.push_back({b, -1}); }
sort(ev.begin(), ev.end());
int cur = 0, best = 0;
for (auto& [t, d] : ev) { cur += d; best = max(best, cur); }
```

```java
int[][] ev = new int[2 * n][];
for (int i = 0; i < n; i++) { ev[2*i] = new int[]{nextInt(), 1}; ev[2*i+1] = new int[]{nextInt(), -1}; }
Arrays.sort(ev, (x, y) -> x[0] != y[0] ? Integer.compare(x[0], y[0]) : Integer.compare(x[1], y[1]));
int cur = 0, best = 0;
for (int[] e : ev) { cur += e[1]; best = Math.max(best, cur); }
```

The tie rule (−1 before +1) treats someone leaving at time t as gone before someone arriving at t. In CSES 1619 all times are distinct, but other problems depend on this choice.

### 4. Merging intervals

[LeetCode 56](https://leetcode.com/problems/merge-intervals/). Sort by start. Keep a current block \[s, e\]. For the next interval \[a, b\]: if a ≤ e, extend e = max(e, b); otherwise save the block and start a new one.

### 5. When greedy fails

Coins {1, 3, 4}, make 6 with the fewest coins. Greedy (largest first) takes 4 + 1 + 1 = 3 coins. The best is 3 + 3 = 2 coins. When a counter-example exists, you need dynamic programming (Lecture 28).

### 6. Common mistakes

- Sorting by the wrong key (start vs end)
- Coding a greedy rule without trying to break it
- Merge Intervals: comparing with the previous interval instead of the current block's end
- Overflow in sums of rewards or times

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Movie Festival](https://cses.fi/problemset/task/1629) | In-class | Easy | Worked above |
| [Restaurant Customers](https://cses.fi/problemset/task/1619) | In-class | Easy | Worked above |
| [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | In-class | Medium | Section 4 |
| [Tasks and Deadlines](https://cses.fi/problemset/task/1630) | Take-home | Easy | Reward = Σ deadline − Σ finish times. Which order makes the finish times smallest? |
| [Missing Coin Sum](https://cses.fi/problemset/task/2183) | Take-home | Medium | Sort. If you can make every sum up to S, when can the next coin extend that? |
| [Alternating Subsequence](https://codeforces.com/problemset/problem/1343/C) | Take-home | Easy | Split into blocks of the same sign; take the best of each |
| [Jump Game II](https://leetcode.com/problems/jump-game-ii/) | Take-home | Medium | Think in layers, like BFS: everything reachable with j jumps |

### Quiz

1. Give a counter-example to “shortest movie first”.
2. Explain the exchange argument for “earliest end first” in two sentences.
3. In Restaurant Customers, what exactly do you sort?
4. Coins {1, 3, 4}, amount 6: what does greedy give, and what is optimal?
5. Missing Coin Sum with coins 1, 2, 4, 9: what is the answer?
