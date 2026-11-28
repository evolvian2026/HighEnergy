# M6 Trees: Student Handbook

Nov 27, 2026 · @Anoop

Trees are graphs with no cycles: n nodes, n − 1 edges, exactly one path between any two nodes. That single path is why so many tree problems have clean recursive answers.

## Lecture 18: Binary trees & BSTs

### 1. Say what the function returns

Before writing any tree recursion, finish this sentence: “f(node) returns … for the subtree rooted at node”. Return one value to the parent; keep the answer for the whole tree in a separate variable.

### 2. Traversals

| Order | Visit | Typical use |
| --- | --- | --- |
| Preorder | node, left, right | Copy or serialise a tree |
| Inorder | left, node, right | A BST gives sorted values |
| Postorder | left, right, node | Compute from children (heights, sums) |
| Level order | by depth, with a queue | Right side view, minimum depth |

### 3. Worked example: Lowest Common Ancestor

[LeetCode 236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/). f(node) returns p or q if it finds one in this subtree, or the LCA once both are found, otherwise null.

```cpp
TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root || root == p || root == q) return root;
    TreeNode* L = lowestCommonAncestor(root->left, p, q);
    TreeNode* R = lowestCommonAncestor(root->right, p, q);
    if (L && R) return root;           // p and q are on different sides
    return L ? L : R;
}
```

```java
public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
    if (root == null || root == p || root == q) return root;
    TreeNode L = lowestCommonAncestor(root.left, p, q);
    TreeNode R = lowestCommonAncestor(root.right, p, q);
    if (L != null && R != null) return root;
    return L != null ? L : R;
}
```

### 4. Worked example: Binary Tree Maximum Path Sum

[LeetCode 124](https://leetcode.com/problems/binary-tree-maximum-path-sum/). A path may bend once, at its highest node.

- gain(node) returns the best **downward** path starting at node: node.val + max(0, gain(left), gain(right)).
- At each node, a bent path left → node → right could be the answer: update the global best.

```cpp
int best = INT_MIN;
int gain(TreeNode* x) {
    if (!x) return 0;
    int l = max(0, gain(x->left)), r = max(0, gain(x->right));
    best = max(best, x->val + l + r);          // path bending at x
    return x->val + max(l, r);                 // only one branch goes up
}
int maxPathSum(TreeNode* root) { gain(root); return best; }
```

```java
int best = Integer.MIN_VALUE;
int gain(TreeNode x) {
    if (x == null) return 0;
    int l = Math.max(0, gain(x.left)), r = Math.max(0, gain(x.right));
    best = Math.max(best, x.val + l + r);
    return x.val + Math.max(l, r);
}
public int maxPathSum(TreeNode root) { gain(root); return best; }
```

### 5. BST checks

A node isn't valid just because it is bigger than its left child: it must be bigger than **everything** in its left subtree. Pass down the allowed range (low, high) and narrow it at each step. Use 64-bit bounds.

### Practice (Lecture 18)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [LCA of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | In-class | Medium | Worked above |
| [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | In-class | Hard | Worked above |
| [Validate BST](https://leetcode.com/problems/validate-binary-search-tree/) | Take-home | Medium | Section 5 |
| [Kth Smallest in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | Take-home | Medium | In-order visits values in sorted order |
| [Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/) | Take-home | Medium | Level order; keep the last node of each level |
| [Construct from Preorder & Inorder](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | Take-home | Medium | Preorder's first value is the root; find it in inorder to split |
| [Serialize and Deserialize](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Take-home | Hard | Preorder with a marker for null |

## Lecture 19: Tree DFS, diameter & subtree DP

### 1. Storing a general tree

Input usually gives n − 1 undirected edges. Store an adjacency list and pass the parent in DFS so you never walk back.

**Deep trees.** A chain of 2 × 10^5 nodes can overflow the recursion stack. Safer: BFS from the root to get an order where parents come first, then process that order backwards for anything computed from children.

### 2. Worked example: Subordinates

[CSES 1674](https://cses.fi/problemset/task/1674). For each employee, count everyone below them = subtree size − 1.

```cpp
vector<vector<int>> ch(n + 1);
for (int i = 2; i <= n; i++) { int b; cin >> b; ch[b].push_back(i); }
vector<int> order = {1}, sz(n + 1, 1);
for (int k = 0; k < (int)order.size(); k++) for (int c : ch[order[k]]) order.push_back(c);   // BFS order
vector<int> par(n + 1, 0);
for (int v = 1; v <= n; v++) for (int c : ch[v]) par[c] = v;
for (int k = n - 1; k > 0; k--) sz[par[order[k]]] += sz[order[k]];
for (int v = 1; v <= n; v++) cout << sz[v] - 1 << ' ';
```

```java
int[] par = new int[n + 1];
List<Integer>[] ch = new ArrayList[n + 1];
for (int i = 1; i <= n; i++) ch[i] = new ArrayList<>();
for (int i = 2; i <= n; i++) { par[i] = nextInt(); ch[par[i]].add(i); }
int[] order = new int[n]; int head = 0, tail = 0; order[tail++] = 1;
while (head < tail) for (int c : ch[order[head++]]) order[tail++] = c;
int[] sz = new int[n + 1]; Arrays.fill(sz, 1);
for (int k = n - 1; k > 0; k--) sz[par[order[k]]] += sz[order[k]];
StringBuilder sb = new StringBuilder();
for (int v = 1; v <= n; v++) sb.append(sz[v] - 1).append(' ');
out.println(sb);
```

### 3. Diameter: the longest path

1. BFS from any node; let u be the farthest node.
2. BFS from u; the farthest distance is the diameter.

Why it works: the farthest node from anywhere is always an end of some longest path.

### 4. Euler tour

Number nodes when DFS enters (tin) and leaves (tout). The subtree of v is exactly the nodes with tin in \[tin\[v\], tout\[v\]\]. This turns subtree questions into range questions (used with Fenwick trees in Lecture 34).

### 5. Rerooting (idea)

Compute an answer for the root, then move the root to each child with a formula. For the sum of distances: ans\[child\] = ans\[parent\] + n − 2 · size\[child\].

### Practice (Lecture 19)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Subordinates](https://cses.fi/problemset/task/1674) | In-class | Easy | Worked above |
| [Tree Diameter](https://cses.fi/problemset/task/1131) | In-class | Medium | Section 3 |
| [Tree Matching](https://cses.fi/problemset/task/1130) | Take-home | Medium | Match greedily from the leaves upwards |
| [Tree Distances I](https://cses.fi/problemset/task/1132) | Take-home | Medium | Farthest node is one of the two diameter ends |
| [Kefa and Park](https://codeforces.com/problemset/problem/580/C) | Take-home | Medium | Carry the current run of cats down the DFS |
| [Linova and Kingdom](https://codeforces.com/problemset/problem/1337/C) | Take-home | Medium | Value of a city = depth − (subtree size − 1) |
| [Tree Distances II](https://cses.fi/problemset/task/1133) | Take-home | Hard | Section 5 |

### Quiz (Lectures 18–19)

1. What does the LCA recursion return for a subtree?
2. Why can't Max Path Sum send left + node + right to the parent?
3. Which traversal of a BST gives sorted values?
4. Describe the two-BFS method for the diameter.
5. Write the rerooting formula for the sum of distances.

## Lecture 20: LCA & binary lifting

### 1. The idea

Store, for every node, its ancestor 1, 2, 4, 8, … levels up:

```latex
up[j][v] = up[j-1][\, up[j-1][v] \,]
```

The 2^j-th ancestor is the 2^(j−1)-th ancestor of the 2^(j−1)-th ancestor. With 18 levels you can jump up to 2^18 > 2 × 10^5 steps. Building the table is O(n log n); each query is O(log n).

### 2. K-th ancestor

Write k in binary and jump once for each set bit. k = 13 = 8 + 4 + 1: jump 8, then 4, then 1.

### 3. Lowest common ancestor

1. Lift the deeper node until both have the same depth.
2. If they are now the same node, that's the LCA.
3. Otherwise, from the biggest jump down to the smallest, jump both nodes whenever their ancestors differ.
4. Their parent is the LCA.

```cpp
const int LOG = 18;
vector<array<int, LOG>> up;   // up[v][j]
vector<int> dep;
int kth(int v, int k) { for (int j = 0; j < LOG && v; j++) if (k >> j & 1) v = up[v][j]; return v; }
int lca(int a, int b) {
    if (dep[a] < dep[b]) swap(a, b);
    a = kth(a, dep[a] - dep[b]);
    if (a == b) return a;
    for (int j = LOG - 1; j >= 0; j--) if (up[a][j] != up[b][j]) { a = up[a][j]; b = up[b][j]; }
    return up[a][0];
}
```

```java
static final int LOG = 18; static int[][] up; static int[] dep;     // up[j][v]
static int kth(int v, int k) { for (int j = 0; j < LOG && v != 0; j++) if ((k >> j & 1) == 1) v = up[j][v]; return v; }
static int lca(int a, int b) {
    if (dep[a] < dep[b]) { int t = a; a = b; b = t; }
    a = kth(a, dep[a] - dep[b]);
    if (a == b) return a;
    for (int j = LOG - 1; j >= 0; j--) if (up[j][a] != up[j][b]) { a = up[j][a]; b = up[j][b]; }
    return up[0][a];
}
```

Use 0 as “no ancestor” (the root's parent is 0 and 0's parent is 0). In [Company Queries I](https://cses.fi/problemset/task/1687), print −1 when the jump lands on 0.

### 4. What LCA unlocks

- Distance: dist(u, v) = depth\[u\] + depth\[v\] − 2 · depth\[lca(u, v)\]
- Add 1 to every node on the path u–v: +1 at u and v, −1 at the LCA and at the LCA's parent, then sum each subtree (Counting Paths)

### Practice (Lecture 20)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Company Queries I](https://cses.fi/problemset/task/1687) | In-class | Medium | Section 2 |
| [Company Queries II](https://cses.fi/problemset/task/1688) | In-class | Medium | Section 3 |
| [Distance Queries](https://cses.fi/problemset/task/1135) | Take-home | Medium | Section 4 |
| [Tree Queries](https://codeforces.com/problemset/problem/1328/E) | Take-home | Hard | Replace each vertex by its parent; then check they all lie on one root path |
| [Counting Paths](https://cses.fi/problemset/task/1136) | Take-home | Hard | Section 4, second bullet |
| [Tree with Maximum Cost](https://codeforces.com/problemset/problem/1092/F) | Take-home | Hard | Rerooting, like Tree Distances II, with weights |

### Quiz (Lecture 20)

1. Write the recurrence for up\[j\]\[v\].
2. How many levels does the table need for n = 2 × 10^5?
3. Write dist(u, v) using the LCA.
4. What is the first step of the LCA algorithm?
5. How do you add 1 to every node on a path with a difference array on a tree?

## Lecture 21: Mid-term contest

Two hours, individual, covering Modules 0–6. Same rules as Contest 1.

### What to revise

| Topic | Lectures | Must be able to |
| --- | --- | --- |
| Complexity, STL / Collections | 1–2 | Pick a data structure from the constraints |
| Prefix sums, two pointers, hashing, greedy | 3–6 | Solve n = 2 × 10^5 array problems in O(n log n) |
| Binary search | 7–8 | Search on the answer with a monotone check |
| Recursion, bits | 9–10 | Enumerate subsets; use masks |
| Stacks, deques, heaps, design | 12–14 | Monotonic stack; heap greedy; LRU |
| Maths | 15–17 | modpow, nCr mod p, sieve |
| Trees | 18–20 | DFS without stack overflow; LCA |

### Contest problems (attempt during the contest; upsolve within 48 hours)

| Problem | Level | Hint after the contest |
| --- | --- | --- |
| [a-Good String](https://codeforces.com/problemset/problem/1385/D) | Medium | Recursion on halves: one half must be all c, the other (c+1)-good |
| [Special Permutation](https://codeforces.com/problemset/problem/1352/G) | Medium | Odd numbers going down, then 4 and 2, then even numbers going up |
| [Towers](https://cses.fi/problemset/task/1073) | Medium | Place each cube on the tower with the smallest top larger than it |
| [Traffic Lights](https://cses.fi/problemset/task/1163) | Medium | Ordered set of positions plus a multiset of gap lengths |

After the contest, compare your result with Contest 1. Write down the two topics that cost you the most time, and redo their take-home problems this week.
