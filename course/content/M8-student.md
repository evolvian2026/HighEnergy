# M8 Dynamic Programming: Student Handbook

Nov 27, 2026 · @Anoop

Dynamic programming = solve each small subproblem once, store it, and build bigger answers from smaller ones. Use the DP card below for every problem in this module.

| Part | Ask yourself |
| --- | --- |
| State | What does dp\[…\] mean, in one sentence? |
| Transition | How do I compute it from smaller states? |
| Base case | Which states do I know directly? |
| Answer | Where is the final answer? |
| Order | In what order do I fill the table? |
| Cost | Number of states × work per state |

## Lecture 28: DP foundations

### 1. From recursion to a table

Fibonacci by plain recursion recomputes the same values exponentially many times. Store each result once (memoisation), or fill an array from small to large (tabulation). Both are O(n). Prefer tabulation: no recursion depth limits.

### 2. Worked example: Frog 1

[AtCoder DP A](https://atcoder.jp/contests/dp/tasks/dp_a). A frog jumps from stone i to i+1 or i+2, paying |h\_i − h\_j|. Minimum total cost to reach stone n?

| Part | Frog 1 |
| --- | --- |
| State | dp\[i\] = minimum cost to reach stone i |
| Transition | dp\[i\] = min(dp\[i−1\] + \|h\_i − h\_{i−1}\|, dp\[i−2\] + \|h\_i − h\_{i−2}\|) |
| Base | dp\[1\] = 0 |
| Answer | dp\[n\] |
| Order | i increasing |

```cpp
vector<long long> dp(n + 1, LLONG_MAX); dp[1] = 0;
for (int i = 2; i <= n; i++) {
    dp[i] = dp[i-1] + abs(h[i] - h[i-1]);
    if (i > 2) dp[i] = min(dp[i], dp[i-2] + abs(h[i] - h[i-2]));
}
cout << dp[n] << '\n';
```

```java
long[] dp = new long[n + 1]; dp[1] = 0;
for (int i = 2; i <= n; i++) {
    dp[i] = dp[i - 1] + Math.abs(h[i] - h[i - 1]);
    if (i > 2) dp[i] = Math.min(dp[i], dp[i - 2] + Math.abs(h[i] - h[i - 2]));
}
out.println(dp[n]);
```

### 3. Counting vs optimising

- **Counting** (how many ways): add the smaller states, modulo 10^9 + 7. [Dice Combinations](https://cses.fi/problemset/task/1633): dp\[s\] = dp\[s−1\] + … + dp\[s−6\], dp\[0\] = 1.
- **Optimising** (min/max): take the best of the smaller states. [Minimizing Coins](https://cses.fi/problemset/task/1634): dp\[s\] = 1 + min over coins c of dp\[s − c\], with dp\[0\] = 0 and “impossible” marked as a large value.

### 4. Loop order changes the meaning

| Problem | Counts | Loops |
| --- | --- | --- |
| [Coin Combinations I](https://cses.fi/problemset/task/1635) | Ordered sequences (2+1 and 1+2 differ) | sums outer, coins inner |
| [Coin Combinations II](https://cses.fi/problemset/task/1636) | Unordered sets | coins outer, sums inner |

### 5. When one index isn't enough

[Vacation](https://atcoder.jp/contests/dp/tasks/dp_c): you can't repeat yesterday's activity. Add it to the state: dp\[i\]\[a\] = best happiness up to day i if day i's activity is a.

### Practice (Lecture 28)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Frog 1](https://atcoder.jp/contests/dp/tasks/dp_a) | In-class | Easy | Worked above |
| [Dice Combinations](https://cses.fi/problemset/task/1633) | In-class | Easy | Section 3 |
| [Minimizing Coins](https://cses.fi/problemset/task/1634) | In-class | Easy | Section 3 |
| [Frog 2](https://atcoder.jp/contests/dp/tasks/dp_b) | Take-home | Easy | Frog 1 with up to k jumps back |
| [Vacation](https://atcoder.jp/contests/dp/tasks/dp_c) | Take-home | Easy | Section 5 |
| [Coin Combinations I](https://cses.fi/problemset/task/1635) | Take-home | Medium | Section 4 |
| [Coin Combinations II](https://cses.fi/problemset/task/1636) | Take-home | Medium | Section 4 |
| [Cut Ribbon](https://codeforces.com/problemset/problem/189/A) | Take-home | Easy | dp\[len\] = most pieces; −∞ if impossible |
| [Boredom](https://codeforces.com/problemset/problem/455/A) | Take-home | Medium | Count each value; taking v forbids v−1 and v+1 |

## Lecture 29: Knapsack & grid DP

### 1. 0/1 knapsack

Each item has weight w and value v and can be taken once. dp\[c\] = best value with capacity c. For each item, loop c **downwards** so the item isn't used twice.

[Book Shop](https://cses.fi/problemset/task/1158): price = weight, pages = value.

```cpp
vector<int> dp(x + 1, 0);
for (int i = 0; i < n; i++)
    for (int c = x; c >= price[i]; c--)
        dp[c] = max(dp[c], dp[c - price[i]] + pages[i]);
cout << dp[x] << '\n';
```

```java
int[] dp = new int[x + 1];
for (int i = 0; i < n; i++)
    for (int c = x; c >= price[i]; c--)
        dp[c] = Math.max(dp[c], dp[c - price[i]] + pages[i]);
out.println(dp[x]);
```

Loop upwards instead and each item can be reused: that's the **unbounded** knapsack (Coin Change).

### 2. Swap what you index by

[Knapsack 2](https://atcoder.jp/contests/dp/tasks/dp_e): capacity up to 10^9 (too big to index) but total value ≤ 10^5. Use dp\[value\] = minimum weight to reach that value; the answer is the largest value with dp ≤ W.

### 3. Grid paths

dp\[i\]\[j\] = dp\[i−1\]\[j\] + dp\[i\]\[j−1\] (paths from above and from the left), 0 on blocked cells, dp\[0\]\[0\] = 1 if free. ([Grid Paths I](https://cses.fi/problemset/task/1638), [Grid 1](https://atcoder.jp/contests/dp/tasks/dp_h).)

### 4. Subset sums

reach\[s\] = can some subset sum to s? Same downward loop as knapsack, with booleans. Partition Equal Subset Sum asks whether total/2 is reachable.

### Practice (Lecture 29)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Knapsack 1](https://atcoder.jp/contests/dp/tasks/dp_d) | In-class | Medium | Section 1, 64-bit values |
| [Knapsack 2](https://atcoder.jp/contests/dp/tasks/dp_e) | In-class | Medium | Section 2 |
| [Book Shop](https://cses.fi/problemset/task/1158) | In-class | Medium | Worked above |
| [Grid 1](https://atcoder.jp/contests/dp/tasks/dp_h) | Take-home | Easy | Section 3 |
| [Grid Paths I](https://cses.fi/problemset/task/1638) | Take-home | Easy | Section 3, mod 10^9 + 7 |
| [Coin Change](https://leetcode.com/problems/coin-change/) | Take-home | Medium | Unbounded: loop upwards |
| [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) | Take-home | Medium | Section 4 |
| [Money Sums](https://cses.fi/problemset/task/1745) | Take-home | Medium | Section 4; print every reachable sum |
| [Two Sets II](https://cses.fi/problemset/task/1093) | Take-home | Medium | Count subsets with sum total/2, then halve with a modular inverse |

### Quiz (Lectures 28–29)

1. What two properties make a problem suitable for DP?
2. Write the transition for Dice Combinations.
3. In Coin Combinations II, which loop goes outside?
4. Why loop capacity downwards in 0/1 knapsack?
5. What is the state in Knapsack 2, and why?

## Lecture 30: Sequence & string DP

### 1. Longest common subsequence

dp\[i\]\[j\] = LCS length of the first i characters of a and the first j of b.

- If a\[i\] = b\[j\]: dp\[i\]\[j\] = dp\[i−1\]\[j−1\] + 1
- Otherwise: dp\[i\]\[j\] = max(dp\[i−1\]\[j\], dp\[i\]\[j−1\])

“abcde” vs “axcye” → 3 (“ace”). To print it, start at dp\[n\]\[m\] and walk back: diagonal when characters match, otherwise towards the larger neighbour; reverse at the end.

### 2. Edit distance

[CSES 1639](https://cses.fi/problemset/task/1639). Fewest insertions, deletions and replacements to turn a into b.

```latex
dp[i][j] = \min\big(dp[i-1][j] + 1,\; dp[i][j-1] + 1,\; dp[i-1][j-1] + [a_i \ne b_j]\big)
```

Base: dp\[i\]\[0\] = i, dp\[0\]\[j\] = j.

```cpp
vector<vector<int>> dp(n + 1, vector<int>(m + 1));
for (int i = 0; i <= n; i++) dp[i][0] = i;
for (int j = 0; j <= m; j++) dp[0][j] = j;
for (int i = 1; i <= n; i++) for (int j = 1; j <= m; j++)
    dp[i][j] = min({dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + (a[i-1] != b[j-1])});
cout << dp[n][m] << '\n';
```

```java
int[][] dp = new int[n + 1][m + 1];
for (int i = 0; i <= n; i++) dp[i][0] = i;
for (int j = 0; j <= m; j++) dp[0][j] = j;
for (int i = 1; i <= n; i++) for (int j = 1; j <= m; j++)
    dp[i][j] = Math.min(Math.min(dp[i-1][j] + 1, dp[i][j-1] + 1), dp[i-1][j-1] + (a.charAt(i-1) != b.charAt(j-1) ? 1 : 0));
out.println(dp[n][m]);
```

### 3. Longest increasing subsequence in O(n log n)

Keep tails\[k\] = the smallest possible last value of an increasing subsequence of length k + 1. For each x, find the first tail ≥ x (lower bound) and replace it with x, or append x if none. The length of tails is the answer. (tails is not itself a valid subsequence.)

```cpp
vector<int> t;
for (int x : a) {
    auto it = lower_bound(t.begin(), t.end(), x);
    if (it == t.end()) t.push_back(x); else *it = x;
}
```

```java
int[] t = new int[n]; int len = 0;
for (int x : a) {
    int lo = -1, hi = len;
    while (hi - lo > 1) { int mid = (lo + hi) >>> 1; if (t[mid] >= x) hi = mid; else lo = mid; }
    t[hi] = x; if (hi == len) len++;
}
```

### 4. Prefix DP on strings

Word Break: ok\[i\] = the first i characters can be split into dictionary words. ok\[0\] = true; ok\[i\] = true if some j < i has ok\[j\] and s\[j..i) in the dictionary.

### Practice (Lecture 30)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [LCS](https://atcoder.jp/contests/dp/tasks/dp_f) | In-class | Medium | Section 1, print the string |
| [Edit Distance](https://cses.fi/problemset/task/1639) | In-class | Medium | Worked above |
| [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) | In-class | Medium | Section 3 |
| [Increasing Subsequence](https://cses.fi/problemset/task/1145) | Take-home | Medium | Section 3, n = 2 × 10^5 |
| [Word Break](https://leetcode.com/problems/word-break/) | Take-home | Medium | Section 4 |
| [Remove One Element](https://codeforces.com/problemset/problem/1272/D) | Take-home | Medium | Increasing-run length ending at i and starting at i; join across one removal |
| [Basketball Exercise](https://codeforces.com/problemset/problem/1195/C) | Take-home | Medium | dp\[i\]\[row of last pick\] |
| [Distinct Subsequences](https://leetcode.com/problems/distinct-subsequences/) | Take-home | Hard | Count ways, LCS-style table |
| [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) | Take-home | Hard | '\*' means zero copies (skip two pattern chars) or one more copy |

## Lecture 31: Interval DP & DP on trees

### 1. Interval DP

State over a range: dp\[l\]\[r\] = best answer for a\[l..r\]. Fill by **increasing length**, so shorter ranges are ready.

**Deque** ([AtCoder DP L](https://atcoder.jp/contests/dp/tasks/dp_l)): two players take from either end. dp\[l\]\[r\] = (my score − opponent's) when it's my turn on a\[l..r\]:

```latex
dp[l][r] = \max(a_l - dp[l+1][r],\; a_r - dp[l][r-1])
```

**Slimes** ([AtCoder DP N](https://atcoder.jp/contests/dp/tasks/dp_n)): merging l..r ends with one final merge at some split k: dp\[l\]\[r\] = min over k of dp\[l\]\[k\] + dp\[k+1\]\[r\] + sum(l..r). O(n³).

**Last-operation trick** (Burst Balloons): instead of choosing what happens first, choose which element is handled **last** in the interval. Then the two sides are independent.

### 2. DP on trees

Compute each node from its children (post-order). Independent Set ([AtCoder DP P](https://atcoder.jp/contests/dp/tasks/dp_p)): count colourings where no two black nodes are adjacent.

- white\[v\] = Π over children (white\[c\] + black\[c\])
- black\[v\] = Π over children white\[c\]

House Robber III is the same shape with max and + instead of + and ×.

### Practice (Lecture 31)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Deque](https://atcoder.jp/contests/dp/tasks/dp_l) | In-class | Medium | Section 1 |
| [Slimes](https://atcoder.jp/contests/dp/tasks/dp_n) | In-class | Medium | Section 1, prefix sums for sum(l..r) |
| [Independent Set](https://atcoder.jp/contests/dp/tasks/dp_p) | In-class | Medium | Section 2 |
| [Removal Game](https://cses.fi/problemset/task/1097) | Take-home | Medium | Like Deque; your score = (total + difference) / 2 |
| [Rectangle Cutting](https://cses.fi/problemset/task/1744) | Take-home | Medium | dp\[w\]\[h\] = min over every horizontal and vertical cut |
| [House Robber III](https://leetcode.com/problems/house-robber-iii/) | Take-home | Medium | Section 2 with max |
| [Burst Balloons](https://leetcode.com/problems/burst-balloons/) | Take-home | Hard | Last-operation trick |
| [Subtree](https://atcoder.jp/contests/dp/tasks/dp_v) | Take-home | Hard | Rerooting with prefix/suffix products of children |

### Quiz (Lectures 30–31)

1. What is the LCS of “abcde” and “axcye”?
2. Name the three edit-distance transitions.
3. For a strictly increasing LIS, lower bound or upper bound?
4. In what order do you fill an interval DP?
5. What does Burst Balloons' “last-operation trick” choose?

## Lecture 32: Bitmask DP & digit DP

### 1. Bitmask DP

When n ≤ 20, the set of items already used fits in a mask, and 2^20 ≈ 10^6 masks is affordable.

**Matching** ([AtCoder DP O](https://atcoder.jp/contests/dp/tasks/dp_o)): match n men with n women (compatible pairs given). dp\[mask\] = ways to match the first popcount(mask) men to exactly the women in mask.

```cpp
vector<long long> dp(1 << n, 0); dp[0] = 1;
for (int mask = 0; mask < (1 << n); mask++) {
    int man = __builtin_popcount(mask);          // next man to match
    if (man >= n || !dp[mask]) continue;
    for (int w = 0; w < n; w++)
        if (ok[man][w] && !(mask >> w & 1)) dp[mask | 1 << w] = (dp[mask | 1 << w] + dp[mask]) % MOD;
}
cout << dp[(1 << n) - 1] << '\n';
```

```java
long[] dp = new long[1 << n]; dp[0] = 1;
for (int mask = 0; mask < (1 << n); mask++) {
    int man = Integer.bitCount(mask);
    if (man >= n || dp[mask] == 0) continue;
    for (int w = 0; w < n; w++)
        if (ok[man][w] && (mask >> w & 1) == 0) dp[mask | 1 << w] = (dp[mask | 1 << w] + dp[mask]) % MOD;
}
out.println(dp[(1 << n) - 1]);
```

**Paths through every node** ([Hamiltonian Flights](https://cses.fi/problemset/task/1690)): dp\[mask\]\[v\] = ways to start at 1, visit exactly mask, and stand at v. About 2 × 10^7 states: use `int` arrays and skip masks without city 1.

### 2. Digit DP

Count numbers ≤ K with some digit property, when K is huge (even 10^10000 as a string). Build the number digit by digit:

- pos: which digit you're choosing
- tight: is the prefix so far equal to K's prefix? If so, the next digit can't exceed K's digit
- state: whatever the property needs (digit sum mod D, previous digit, count of non-zero digits…)

To count in \[L, R\], compute f(R) − f(L − 1).

### Practice (Lecture 32)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Matching](https://atcoder.jp/contests/dp/tasks/dp_o) | In-class | Hard | Worked above |
| [Hamiltonian Flights](https://cses.fi/problemset/task/1690) | In-class | Hard | Section 1 |
| [Digit Sum](https://atcoder.jp/contests/dp/tasks/dp_s) | In-class | Hard | state = digit sum mod D; subtract 1 for the number 0 |
| [Elevator Rides](https://cses.fi/problemset/task/1653) | Take-home | Hard | dp\[mask\] = (rides used, weight in the current ride) |
| [Kefa and Dishes](https://codeforces.com/problemset/problem/580/D) | Take-home | Hard | dp\[mask\]\[last dish\] |
| [Counting Numbers](https://cses.fi/problemset/task/2220) | Take-home | Hard | State = previous digit; handle leading zeros |
| [Classy Numbers](https://codeforces.com/problemset/problem/1036/C) | Take-home | Hard | State = non-zero digits used so far (≤ 3) |

## Lecture 33: Probability & game DP + Contest 3

### 1. Probability DP

[Coins](https://atcoder.jp/contests/dp/tasks/dp_i): coin i shows heads with probability p\_i. dp\[i\]\[j\] = probability of exactly j heads among the first i coins: dp\[i\]\[j\] = dp\[i−1\]\[j−1\] · p\_i + dp\[i−1\]\[j\] · (1 − p\_i). Use `double` and print with enough decimals.

### 2. Game DP

[Stones](https://atcoder.jp/contests/dp/tasks/dp_k): win\[x\] is true if some allowed move a leads to a position where the opponent loses (win\[x − a\] false). Fill x from 0 upwards.

### 3. Expected value DP

[Sushi](https://atcoder.jp/contests/dp/tasks/dp_j): the state is how many plates have 1, 2 and 3 pieces. Picking an empty plate keeps you in the same state; solve that self-loop with algebra (E = 1 + p·E + … → rearrange for E).

### 4. Contest 3

90 minutes, DP only, four AtCoder DP Contest tasks not assigned so far. Fill the DP card on paper before you code each one. Upsolve within 48 hours.

### Practice (Lecture 33)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Coins](https://atcoder.jp/contests/dp/tasks/dp_i) | In-class | Medium | Section 1 |
| [Stones](https://atcoder.jp/contests/dp/tasks/dp_k) | In-class | Medium | Section 2 |
| [k-Tree](https://codeforces.com/problemset/problem/431/C) | Take-home | Medium | dp\[sum\]\[used an edge ≥ d yet?\] |
| [Sleeping Schedule](https://codeforces.com/problemset/problem/1324/E) | Take-home | Medium | dp\[i\]\[current time mod h\] |
| [Sushi](https://atcoder.jp/contests/dp/tasks/dp_j) | Take-home | Hard | Section 3 |
| [Projects](https://cses.fi/problemset/task/1140) | Take-home | Hard | Sort by end; binary search the last compatible project |
| [Counting Towers](https://cses.fi/problemset/task/2413) | Take-home | Hard | Two states per row: top row joined or split |
| [Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/) | Take-home | Hard | dp\[transactions used\]\[holding a share?\] |

### Quiz (Lectures 32–33)

1. In Matching, what does dp\[mask\] count?
2. What does the tight flag mean in digit DP?
3. How do you count numbers in \[L, R\] with digit DP?
4. Write the Coins transition.
5. When is a game position x winning?
