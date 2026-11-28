# M2 Binary Search: Student Handbook

Nov 27, 2026 · @Anoop

Binary search needs only one thing: a yes/no question whose answers go no, no, …, no, yes, yes, …, yes. This module teaches one template for it and uses it everywhere.

## Lecture 7: Binary search fundamentals

Halving the search range every step finds an answer among 10^9 possibilities in about 30 steps.

### 1. The “first true” template

Suppose ok(x) is false for small x and true from some point on. We want the first x where it is true.

```text
// invariant: ok(lo) is false, ok(hi) is true
while hi - lo > 1:
    mid = lo + (hi - lo) / 2
    if ok(mid): hi = mid
    else:       lo = mid
answer = hi
```

Why it always works:

- mid is strictly between lo and hi, so the gap shrinks every step and the loop ends.
- The invariant never breaks, so when the gap is 1, hi is the first true position.
- If no real value is false, start lo one below the range (a “sentinel”), for example lo = −1 for array indices.

### 2. Lower bound and upper bound

On a sorted array a\[0..n−1\] with lo = −1 and hi = n:

| You want | ok(i) | a = \[1, 3, 3, 5, 8\], x = 3 |
| --- | --- | --- |
| First index with a\[i\] ≥ x (lower bound) | a\[i\] ≥ x | 1 |
| First index with a\[i\] > x (upper bound) | a\[i\] > x | 3 |
| How many equal x | upper − lower | 2 |
| How many in \[L, R\] | upper(R) − lower(L) |  |

```cpp
int lb = lower_bound(a.begin(), a.end(), x) - a.begin();
int ub = upper_bound(a.begin(), a.end(), x) - a.begin();
```

```java
// Java has no lower_bound for arrays: write it once and reuse it
static int lowerBound(long[] a, long x) {
    int lo = -1, hi = a.length;              // a[lo] < x, a[hi] >= x (sentinels)
    while (hi - lo > 1) {
        int mid = (lo + hi) >>> 1;
        if (a[mid] >= x) hi = mid; else lo = mid;
    }
    return hi;
}
```

Upper bound is the same with `a[mid] > x`.

### 3. Worked example: Worms

[Codeforces 474B](https://codeforces.com/problemset/problem/474/B). Worms are numbered across piles: pile 1 has labels 1..a\_1, pile 2 continues from there, and so on. For each label q, print its pile.

**Idea.** With prefix sums p, pile i holds labels p\[i−1\] + 1 .. p\[i\]. The answer is the first i with p\[i\] ≥ q: a lower bound.

**Dry run.** a = \[2, 7, 3, 4, 9\]. p = \[0, 2, 9, 12, 16, 25\]. Label 1 → pile 1; label 25 → pile 5; label 11 → pile 3.

```cpp
vector<long long> p(n + 1, 0);
for (int i = 1; i <= n; i++) { long long x; cin >> x; p[i] = p[i-1] + x; }
int m; cin >> m;
while (m--) {
    long long q; cin >> q;
    cout << lower_bound(p.begin() + 1, p.end(), q) - p.begin() << '\n';
}
```

```java
long[] p = new long[n + 1];
for (int i = 1; i <= n; i++) p[i] = p[i - 1] + nextLong();
int m = nextInt();
while (m-- > 0) {
    long q = nextLong();
    int lo = 0, hi = n;                       // p[0] = 0 < q, p[n] >= q
    while (hi - lo > 1) { int mid = (lo + hi) >>> 1; if (p[mid] >= q) hi = mid; else lo = mid; }
    out.println(hi);
}
```

### 4. Worked example: Search in Rotated Sorted Array

[LeetCode 33](https://leetcode.com/problems/search-in-rotated-sorted-array/). A sorted array of distinct values was rotated, like \[4, 5, 6, 7, 0, 1, 2\]. Find the index of target, or −1, in O(log n).

**Idea.** Cut at mid. At least one half is still sorted. Check whether target lies inside the sorted half's range; if yes go there, otherwise go to the other half.

```cpp
int search(vector<int>& a, int target) {
    int lo = 0, hi = (int)a.size() - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[lo] <= a[mid]) {                       // left half sorted
            if (a[lo] <= target && target < a[mid]) hi = mid - 1; else lo = mid + 1;
        } else {                                     // right half sorted
            if (a[mid] < target && target <= a[hi]) lo = mid + 1; else hi = mid - 1;
        }
    }
    return -1;
}
```

```java
public int search(int[] a, int target) {
    int lo = 0, hi = a.length - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == target) return mid;
        if (a[lo] <= a[mid]) {
            if (a[lo] <= target && target < a[mid]) hi = mid - 1; else lo = mid + 1;
        } else {
            if (a[mid] < target && target <= a[hi]) lo = mid + 1; else hi = mid - 1;
        }
    }
    return -1;
}
```

This one uses the classic “closed range” loop because it looks for an exact value, not a first-true position. Use `<=` in `a[lo] <= a[mid]` so a two-element range works.

### 5. Common mistakes

- Mixing loop styles (`lo < hi` with `hi = mid − 1` from another template)
- `mid = (lo + hi) / 2` overflowing when lo and hi are near 2 × 10^9
- Java's `Arrays.binarySearch` on arrays with duplicates: it returns any matching index
- A linear scan per query when there are 10^5 queries

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) | In-class | Medium | Worked above |
| [Worms](https://codeforces.com/problemset/problem/474/B) | In-class | Easy | Worked above |
| [Cellular Network](https://codeforces.com/problemset/problem/702/C) | Take-home | Medium | For each city, find the nearest tower on each side with a lower bound |
| [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | Take-home | Medium | Compare each element with the last one. That predicate is monotone |
| [Median of Two Sorted Arrays](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Take-home | Hard | Binary search where to cut the smaller array |
| [Pair of Topics](https://codeforces.com/problemset/problem/1324/D) | Take-home | Medium | Let c = a − b. Count pairs with c\_i + c\_j > 0 after sorting |

### Quiz

1. What does binary search actually need: a sorted array, or something more general?
2. State the invariant of the first-true template.
3. For a = \[1, 3, 3, 5, 8\], what are the lower and upper bounds of 3?
4. Why write lo + (hi − lo)/2?
5. In a rotated array, how can you tell the left half is sorted?

## Lecture 8: Binary search on the answer

When a problem asks for “the minimum T such that something is possible”, don't compute T directly. Write a check `can(T)` and binary search over T.

### 1. Spot the pattern

Look for these phrases:

- “minimum time / speed / capacity needed to…”
- “minimise the largest…” or “maximise the smallest…”
- an answer range far too large to try every value (up to 10^9 or 10^18)

Then check that `can(T)` is **monotone**: if T works, every bigger T works too.

### 2. The recipe

1. Write `can(T)`, usually a greedy O(n) check.
2. Pick lo where `can(lo)` is surely false (or a sentinel such as 0) and hi where `can(hi)` is surely true.
3. Run the first-true template from Lecture 7 on T.

Total time: O(n × log(hi − lo)). For a range of 10^18 that's about 60 checks.

### 3. Worked example: Factory Machines

[CSES 1620](https://cses.fi/problemset/task/1620). Machine i makes one product every k\_i seconds; all run in parallel. Minimum time to make t products?

**Check.** In T seconds machine i makes ⌊T / k\_i⌋ products. can(T) = Σ ⌊T / k\_i⌋ ≥ t. More time never makes fewer products, so it is monotone.

**Bounds.** lo = 0 (nothing is made). hi = min(k) × t: the fastest machine alone finishes by then.

**Dry run.** k = \[3, 2, 5\], t = 7.

| T | made = T/3 + T/2 + T/5 | can(T)? |
| --- | --- | --- |
| 7 | 2 + 3 + 1 = 6 | no |
| 8 | 2 + 4 + 1 = 7 | yes |

Answer 8.

**Overflow trap.** With T near 10^18 and k\_i = 1, the sum can pass 64 bits. Stop adding as soon as the total reaches t.

```cpp
int n; long long t; cin >> n >> t;
vector<long long> k(n);
for (auto& x : k) cin >> x;
auto can = [&](long long T) {
    long long made = 0;
    for (long long x : k) { made += T / x; if (made >= t) return true; }
    return false;
};
long long lo = 0, hi = *min_element(k.begin(), k.end()) * t;
while (hi - lo > 1) {
    long long mid = lo + (hi - lo) / 2;
    if (can(mid)) hi = mid; else lo = mid;
}
cout << hi << '\n';
```

```java
int n = nextInt(); long t = nextLong();
long[] k = new long[n];
long minK = Long.MAX_VALUE;
for (int i = 0; i < n; i++) { k[i] = nextLong(); minK = Math.min(minK, k[i]); }
long lo = 0, hi = minK * t;
while (hi - lo > 1) {
    long mid = lo + (hi - lo) / 2, made = 0;
    boolean ok = false;
    for (long x : k) { made += mid / x; if (made >= t) { ok = true; break; } }
    if (ok) hi = mid; else lo = mid;
}
out.println(hi);
```

### 4. Worked example: Koko Eating Bananas

[LeetCode 875](https://leetcode.com/problems/koko-eating-bananas/). Piles p\_i; each hour Koko eats up to s bananas from one pile. Smallest s to finish within h hours?

can(s) = Σ ⌈p\_i / s⌉ ≤ h. Compute the ceiling with integers: (p + s − 1) / s. lo = 0, hi = max(p).

```cpp
int minEatingSpeed(vector<int>& piles, int h) {
    long long lo = 0, hi = *max_element(piles.begin(), piles.end());
    while (hi - lo > 1) {
        long long s = lo + (hi - lo) / 2, hours = 0;
        for (int p : piles) hours += (p + s - 1) / s;
        if (hours <= h) hi = s; else lo = s;
    }
    return (int)hi;
}
```

```java
public int minEatingSpeed(int[] piles, int h) {
    long lo = 0, hi = 0;
    for (int p : piles) hi = Math.max(hi, p);
    while (hi - lo > 1) {
        long s = lo + (hi - lo) / 2, hours = 0;
        for (int p : piles) hours += (p + s - 1) / s;
        if (hours <= h) hi = s; else lo = s;
    }
    return (int) hi;
}
```

### 5. Minimise the maximum: Array Division

[CSES 1085](https://cses.fi/problemset/task/1085). Split the array into k contiguous parts so the largest part sum is as small as possible.

can(S): walk left to right, start a new part whenever adding the next number would exceed S, and count parts. Feasible if parts ≤ k. lo = max(a) − 1 (a part must hold the biggest element), hi = sum of all.

### 6. Ternary search (for reference)

If f(x) goes down and then up (unimodal), compare f(m1) and f(m2) at two inner points and drop the worse third. On integers, a simpler and safer alternative is binary search on the slope: first x with f(x + 1) − f(x) ≥ 0. Avoid both on functions with flat stretches.

### 7. Common mistakes

- `int` for T, sums or products
- hi too small (wrong answer) or a sum that overflows (no early stop)
- A check that isn't monotone, often testing “exactly k” instead of “at most k”
- Forgetting that a part must be at least max(a) in Array Division

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Factory Machines](https://cses.fi/problemset/task/1620) | In-class | Medium | Worked above |
| [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | In-class | Medium | Worked above |
| [Array Division](https://cses.fi/problemset/task/1085) | Take-home | Medium | Section 5 |
| [Maximum Median](https://codeforces.com/problemset/problem/1201/C) | Take-home | Medium | Sort. To make the median at least m, raise every element from the middle up to m |
| [Split Array Largest Sum](https://leetcode.com/problems/split-array-largest-sum/) | Take-home | Hard | Same idea as Array Division |
| [Magic Ship](https://codeforces.com/problemset/problem/1117/C) | Take-home | Hard | Search on the number of days. The wind's total push after d days is easy to compute |

### Quiz

1. What must be true of can(T) for answer search to work?
2. Factory Machines with k = \[3, 2, 5\] and t = 7: what is the answer?
3. Give a safe upper bound hi for Factory Machines.
4. How do you avoid overflow inside the Factory Machines check?
5. In Array Division, what is the smallest value S can possibly take?
