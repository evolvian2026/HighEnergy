# M9 Range Queries: Student Handbook

Nov 27, 2026 · @Anoop

## Lecture 34: Sparse table & Fenwick tree

### 1. Which tool?

| Need | Tool | Query | Update |
| --- | --- | --- | --- |
| Sum, array never changes | Prefix sums | O(1) | — |
| Min/max, array never changes | Sparse table | O(1) | — |
| Sum, single values change | Fenwick tree (BIT) | O(log n) | O(log n) |
| Min/max/custom, single values change | Segment tree | O(log n) | O(log n) |
| Whole ranges change | Segment tree with lazy | O(log n) | O(log n) |

### 2. Sparse table

st\[k\]\[i\] = min of a\[i .. i + 2^k − 1\], built as min(st\[k−1\]\[i\], st\[k−1\]\[i + 2^(k−1)\]). For a query \[l, r\], take k = ⌊log2(r − l + 1)⌋ and combine two blocks that overlap: min(st\[k\]\[l\], st\[k\]\[r − 2^k + 1\]). Overlap is fine for min/max, not for sums. ([CSES 1647](https://cses.fi/problemset/task/1647))

### 3. Fenwick tree

Position i (1-based) stores the sum of the last (i & −i) elements ending at i. Prefix sums walk down by removing the lowest bit; updates walk up by adding it.

```cpp
struct BIT {
    int n; vector<long long> t;
    BIT(int n) : n(n), t(n + 1, 0) {}
    void add(int i, long long v) { for (; i <= n; i += i & -i) t[i] += v; }
    long long sum(int i) { long long s = 0; for (; i > 0; i -= i & -i) s += t[i]; return s; }
    long long sum(int l, int r) { return sum(r) - sum(l - 1); }
};
```

```java
static long[] t; static int N;
static void add(int i, long v) { for (; i <= N; i += i & -i) t[i] += v; }
static long sum(int i) { long s = 0; for (; i > 0; i -= i & -i) s += t[i]; return s; }
static long sum(int l, int r) { return sum(r) - sum(l - 1); }
```

**Dynamic Range Sum Queries** ([CSES 1648](https://cses.fi/problemset/task/1648)): “set position k to u” becomes add(k, u − a\[k\]); then a\[k\] = u.

### 4. Fenwick tricks

- **Range add, point query:** keep a BIT on the difference array: add(l, v), add(r + 1, −v); the value at i is sum(i). ([Range Update Queries](https://cses.fi/problemset/task/1651))
- **Counting smaller elements:** compress values to ranks 1..n, scan from the right, query sum(rank − 1), then add(rank, 1).
- **Subtree sums:** with an Euler tour (Lecture 19) each subtree is a contiguous range.

## Lecture 35: Segment tree & lazy propagation

### 1. The structure

A binary tree over the array: each node stores the answer for its range, combined from its two children. Query by covering \[l, r\] with O(log n) nodes; update a leaf and fix its ancestors.

```cpp
int n; vector<long long> tr;            // size 4n, recursive
void update(int node, int l, int r, int pos, long long val) {
    if (l == r) { tr[node] = val; return; }
    int m = (l + r) / 2;
    if (pos <= m) update(2*node, l, m, pos, val); else update(2*node+1, m+1, r, pos, val);
    tr[node] = min(tr[2*node], tr[2*node+1]);
}
long long query(int node, int l, int r, int ql, int qr) {
    if (qr < l || r < ql) return LLONG_MAX;
    if (ql <= l && r <= qr) return tr[node];
    int m = (l + r) / 2;
    return min(query(2*node, l, m, ql, qr), query(2*node+1, m+1, r, ql, qr));
}
```

```java
static long[] tr;                       // size 4n
static void update(int node, int l, int r, int pos, long val) {
    if (l == r) { tr[node] = val; return; }
    int m = (l + r) / 2;
    if (pos <= m) update(2*node, l, m, pos, val); else update(2*node+1, m+1, r, pos, val);
    tr[node] = Math.min(tr[2*node], tr[2*node+1]);
}
static long query(int node, int l, int r, int ql, int qr) {
    if (qr < l || r < ql) return Long.MAX_VALUE;
    if (ql <= l && r <= qr) return tr[node];
    int m = (l + r) / 2;
    return Math.min(query(2*node, l, m, ql, qr), query(2*node+1, m+1, r, ql, qr));
}
```

### 2. Walking down the tree

[Hotel Queries](https://cses.fi/problemset/task/1143): find the first hotel with at least x free rooms. Store the maximum per node; from the root, go left if the left child's maximum ≥ x, otherwise right. O(log n), no binary search needed.

### 3. Designing your own node

Ask: what must each node store so two neighbours can be merged? For the best subarray sum ([Subarray Sum Queries](https://cses.fi/problemset/task/1190)), store sum, best prefix, best suffix and best:

- best = max(L.best, R.best, L.suffix + R.prefix)
- prefix = max(L.prefix, L.sum + R.prefix), suffix = max(R.suffix, R.sum + L.suffix)

### 4. Lazy propagation

To add v to a whole range, don't touch every leaf. Mark the covering nodes with a pending “+v” (the lazy tag) and update their stored value. Before visiting a node's children, push its tag down. If you support both “add” and “set”, a set overrides any pending add.

### Practice

| Problem | Lecture | Type | Level | Hint |
| --- | --- | --- | --- | --- |
| [Static Range Minimum Queries](https://cses.fi/problemset/task/1647) | 34 | In-class | Easy | Sparse table |
| [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) | 34 | In-class | Medium | BIT |
| [Range Update Queries](https://cses.fi/problemset/task/1651) | 34 | Take-home | Medium | BIT on differences |
| [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) | 34 | Take-home | Medium | BIT |
| [Count of Smaller Numbers After Self](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) | 34 | Take-home | Hard | Compress, scan from the right |
| [Enemy is weak](https://codeforces.com/problemset/problem/61/E) | 34 | Take-home | Hard | For each j: greater on the left × smaller on the right |
| [Subtree Queries](https://cses.fi/problemset/task/1137) | 34 | Take-home | Hard | Euler tour + BIT |
| [Dynamic Range Minimum Queries](https://cses.fi/problemset/task/1649) | 35 | In-class | Medium | Section 1 |
| [Hotel Queries](https://cses.fi/problemset/task/1143) | 35 | In-class | Medium | Section 2 |
| [Xenia and Bit Operations](https://codeforces.com/problemset/problem/339/D) | 35 | Take-home | Medium | Alternate OR and XOR by level |
| [Distinct Characters Queries](https://codeforces.com/problemset/problem/1234/D) | 35 | Take-home | Medium | Each node stores a 26-bit mask; merge with OR |
| [Subarray Sum Queries](https://cses.fi/problemset/task/1190) | 35 | Take-home | Hard | Section 3 |
| [Sereja and Brackets](https://codeforces.com/problemset/problem/380/C) | 35 | Take-home | Hard | Node = (matched, unmatched open, unmatched close) |
| [Range Updates and Sums](https://cses.fi/problemset/task/1735) | 35 | Take-home | Hard | Section 4 with add and set |
| [Salary Queries](https://cses.fi/problemset/task/1144) | 35 | Take-home | Hard | Read all queries first; compress every salary value |

### Quiz

1. Why can a sparse table answer range minimum but not range sum in O(1)?
2. What does i & −i mean in a Fenwick tree?
3. How do you “set a\[k\] = u” with a BIT that only supports add?
4. How big must the array be for a recursive segment tree?
5. Write the merge rule for the best subarray sum.
