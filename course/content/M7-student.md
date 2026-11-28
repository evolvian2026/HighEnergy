# M7 Graphs: Student Handbook

Nov 27, 2026 · @Anoop

First question for every graph problem: what are the nodes, what are the edges, are edges directed, and do they have weights? Once you can answer that, the algorithm usually follows.

## Lecture 22: Graph basics, BFS/DFS & grids

### 1. Storing a graph

Use an adjacency list: for each node, the list of its neighbours. Memory O(n + m). An adjacency matrix (n × n) only works for n up to a few thousand.

```cpp
vector<vector<int>> g(n + 1);
for (int i = 0; i < m; i++) { int a, b; cin >> a >> b; g[a].push_back(b); g[b].push_back(a); }
```

```java
List<Integer>[] g = new ArrayList[n + 1];
for (int i = 1; i <= n; i++) g[i] = new ArrayList<>();
for (int i = 0; i < m; i++) { int a = nextInt(), b = nextInt(); g[a].add(b); g[b].add(a); }
```

### 2. BFS: shortest paths when every edge costs the same

BFS visits nodes in order of distance. Mark a node visited when you push it. Keep `parent` to rebuild the path.

```cpp
vector<int> dist(n + 1, -1), par(n + 1, 0); queue<int> q; dist[s] = 0; q.push(s);
while (!q.empty()) { int u = q.front(); q.pop();
    for (int v : g[u]) if (dist[v] == -1) { dist[v] = dist[u] + 1; par[v] = u; q.push(v); } }
```

```java
int[] dist = new int[n + 1], par = new int[n + 1]; Arrays.fill(dist, -1);
ArrayDeque<Integer> q = new ArrayDeque<>(); dist[s] = 0; q.add(s);
while (!q.isEmpty()) { int u = q.poll();
    for (int v : g[u]) if (dist[v] == -1) { dist[v] = dist[u] + 1; par[v] = u; q.add(v); } }
```

To print the path to t: follow par from t back to s, then reverse.

### 3. Grids are graphs

Each cell is a node; neighbours are up, down, left, right. Use direction arrays and a bounds check.

- **Counting Rooms** ([CSES 1192](https://cses.fi/problemset/task/1192)): count how many times you start a new BFS/flood fill from an unvisited floor cell.
- **Labyrinth** ([CSES 1193](https://cses.fi/problemset/task/1193)): BFS from A; remember the direction letter used to enter each cell; walk back from B and reverse the letters.

Avoid recursive flood fill on a 1000 × 1000 grid: a million nested calls overflow the stack.

### 4. Multi-source BFS and bipartite graphs

- Start BFS with **all** sources in the queue at distance 0 (Rotting Oranges, Monsters).
- A graph is bipartite if you can colour nodes with two colours so every edge joins different colours. BFS colouring finds a conflict if it isn't (Building Teams).

### 5. Implicit graphs

Sometimes the graph isn't given. In Word Ladder each word is a node and two words are joined when they differ in one letter. BFS still works.

### Practice (Lecture 22)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Counting Rooms](https://cses.fi/problemset/task/1192) | In-class | Easy | Section 3 |
| [Labyrinth](https://cses.fi/problemset/task/1193) | In-class | Medium | Section 3 |
| [Number of Islands](https://leetcode.com/problems/number-of-islands/) | In-class | Medium | Same as Counting Rooms |
| [Building Roads](https://cses.fi/problemset/task/1666) | Take-home | Easy | Count components; connect one node of each |
| [Building Teams](https://cses.fi/problemset/task/1668) | Take-home | Medium | Section 4 |
| [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) | Take-home | Medium | Multi-source BFS |
| [Solve The Maze](https://codeforces.com/problemset/problem/1365/D) | Take-home | Medium | Block every empty cell next to a bad person, then BFS from the exit |
| [Monsters](https://cses.fi/problemset/task/1194) | Take-home | Hard | BFS monster times first; you must arrive strictly earlier |
| [Word Ladder](https://leetcode.com/problems/word-ladder/) | Take-home | Hard | Section 5 |

## Lecture 23: Topological sort, cycles & DAG DP

### 1. Topological order (Kahn's algorithm)

Order tasks so every task comes after its prerequisites.

1. Count incoming edges (in-degree) for every node.
2. Put all nodes with in-degree 0 in a queue.
3. Pop a node, add it to the order, and decrease its neighbours' in-degrees; push any that reach 0.
4. If fewer than n nodes come out, there is a cycle: no valid order.

**Course Schedule** ([CSES 1679](https://cses.fi/problemset/task/1679)) is exactly this; print IMPOSSIBLE on a cycle.

```cpp
vector<int> indeg(n + 1, 0), order;
for (int u = 1; u <= n; u++) for (int v : g[u]) indeg[v]++;
queue<int> q; for (int u = 1; u <= n; u++) if (indeg[u] == 0) q.push(u);
while (!q.empty()) { int u = q.front(); q.pop(); order.push_back(u);
    for (int v : g[u]) if (--indeg[v] == 0) q.push(v); }
```

```java
int[] indeg = new int[n + 1];
for (int u = 1; u <= n; u++) for (int v : g[u]) indeg[v]++;
ArrayDeque<Integer> q = new ArrayDeque<>(); for (int u = 1; u <= n; u++) if (indeg[u] == 0) q.add(u);
List<Integer> order = new ArrayList<>();
while (!q.isEmpty()) { int u = q.poll(); order.add(u);
    for (int v : g[u]) if (--indeg[v] == 0) q.add(v); }
```

### 2. Finding cycles

- **Undirected:** during DFS, reaching a visited node that isn't your parent means a cycle.
- **Directed:** colour nodes white (new), grey (on the current DFS path), black (finished). An edge to a grey node is a cycle. Keep parents to print it.

### 3. DP on a DAG

Process nodes in topological order; every predecessor is finished before you use it.

- Longest path: best\[v\] = max over edges u → v of best\[u\] + 1
- Number of paths from 1: ways\[v\] = sum over edges u → v of ways\[u\]
- Mark nodes unreachable from the start as −∞, not 0 (Longest Flight Route)

### Practice (Lecture 23)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Course Schedule](https://cses.fi/problemset/task/1679) | In-class | Medium | Section 1 |
| [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) | In-class | Medium | Section 1 |
| [Round Trip](https://cses.fi/problemset/task/1669) | Take-home | Medium | Undirected cycle, print it |
| [Round Trip II](https://cses.fi/problemset/task/1678) | Take-home | Medium | Directed cycle with colours |
| [Longest Flight Route](https://cses.fi/problemset/task/1680) | Take-home | Medium | Section 3 with a parent array |
| [Longest Path (AtCoder)](https://atcoder.jp/contests/dp/tasks/dp_g) | Take-home | Medium | Section 3 |
| [Fox And Names](https://codeforces.com/problemset/problem/510/C) | Take-home | Medium | Compare neighbouring names to get letter edges; watch prefixes |

### Quiz (Lectures 22–23)

1. When does BFS find shortest paths?
2. When should you mark a node visited in BFS?
3. How do you test if a graph is bipartite?
4. How does Kahn's algorithm tell you there is a cycle?
5. In which order must DP on a DAG process nodes?

## Lecture 24: Shortest paths

### 1. Pick the algorithm

| Situation | Use | Time |
| --- | --- | --- |
| All edges cost the same | BFS | O(n + m) |
| Edge costs are 0 or 1 | 0-1 BFS (deque: 0-edges to the front) | O(n + m) |
| Costs ≥ 0 | Dijkstra | O(m log n) |
| Negative costs, or detect negative cycles | Bellman–Ford | O(n · m) |
| Every pair of nodes, n ≤ 500 | Floyd–Warshall | O(n³) |

### 2. Dijkstra

Always expand the closest unfinished node. With a priority queue, push (distance, node) whenever you improve a distance, and skip entries that are out of date when popped.

**Shortest Routes I** ([CSES 1671](https://cses.fi/problemset/task/1671)): distances from city 1 to all cities. Use 64-bit distances.

```cpp
vector<long long> dist(n + 1, LLONG_MAX); dist[1] = 0;
priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq; pq.push({0, 1});
while (!pq.empty()) {
    auto [d, u] = pq.top(); pq.pop();
    if (d > dist[u]) continue;                         // out-of-date entry
    for (auto [v, w] : g[u])
        if (d + w < dist[v]) { dist[v] = d + w; pq.push({dist[v], v}); }
}
```

```java
long[] dist = new long[n + 1]; Arrays.fill(dist, Long.MAX_VALUE); dist[1] = 0;
PriorityQueue<long[]> pq = new PriorityQueue<>((x, y) -> Long.compare(x[0], y[0]));
pq.add(new long[]{0, 1});
while (!pq.isEmpty()) {
    long[] t = pq.poll(); long d = t[0]; int u = (int) t[1];
    if (d > dist[u]) continue;
    for (int[] e : g[u]) { int v = e[0]; long w = e[1];
        if (d + w < dist[v]) { dist[v] = d + w; pq.add(new long[]{dist[v], v}); } }
}
```

Negative edges break Dijkstra: a node already finished might later be reachable more cheaply.

### 3. Floyd–Warshall

dist\[i\]\[j\] = min(dist\[i\]\[j\], dist\[i\]\[k\] + dist\[k\]\[j\]) with **k in the outer loop**. Answers all pairs ([Shortest Routes II](https://cses.fi/problemset/task/1672)).

### 4. Bellman–Ford

Relax every edge n − 1 times. If anything still improves in an n-th round, a negative cycle exists. In [High Score](https://cses.fi/problemset/task/1673) a bad cycle only matters if it can reach the destination.

### 5. Extra state = bigger graph

[Flight Discount](https://cses.fi/problemset/task/1195): you may halve one flight. Use states (city, used coupon?) and run Dijkstra on 2n states. The same trick handles “at most k stops” or “with a key”.

### Practice (Lecture 24)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Shortest Routes I](https://cses.fi/problemset/task/1671) | In-class | Medium | Section 2 |
| [Shortest Routes II](https://cses.fi/problemset/task/1672) | In-class | Medium | Section 3 |
| [Network Delay Time](https://leetcode.com/problems/network-delay-time/) | Take-home | Medium | Dijkstra; answer is the largest distance |
| [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | Take-home | Medium | Bellman–Ford for k + 1 rounds, copying distances each round |
| [Flight Discount](https://cses.fi/problemset/task/1195) | Take-home | Medium | Section 5 |
| [Dijkstra?](https://codeforces.com/problemset/problem/20/C) | Take-home | Medium | Dijkstra with a parent array |
| [High Score](https://cses.fi/problemset/task/1673) | Take-home | Hard | Section 4 |
| [Cycle Finding](https://cses.fi/problemset/task/1197) | Take-home | Hard | Bellman–Ford; walk back n steps from the last relaxed node to land in the cycle |
| [Labyrinth (Codeforces)](https://codeforces.com/problemset/problem/1063/B) | Take-home | Hard | Up/down moves are free, left/right limited: 0-1 BFS |

## Lecture 25: DSU & minimum spanning trees

### 1. Disjoint Set Union

Keeps track of which items are in the same group, with almost O(1) `find` and `unite`.

```cpp
struct DSU {
    vector<int> p, sz;
    DSU(int n) : p(n + 1), sz(n + 1, 1) { iota(p.begin(), p.end(), 0); }
    int find(int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; }
    bool unite(int a, int b) {
        a = find(a); b = find(b); if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        p[b] = a; sz[a] += sz[b]; return true;
    }
};
```

```java
static int[] p, sz;
static int find(int x) { while (p[x] != x) { p[x] = p[p[x]]; x = p[x]; } return x; }
static boolean unite(int a, int b) {
    a = find(a); b = find(b); if (a == b) return false;
    if (sz[a] < sz[b]) { int t = a; a = b; b = t; }
    p[b] = a; sz[a] += sz[b]; return true;
}
```

**Road Construction** ([CSES 1676](https://cses.fi/problemset/task/1676)): after each road, print the number of components and the largest component size. Every successful unite reduces the count by 1.

### 2. Minimum spanning tree (Kruskal)

Connect all n nodes with n − 1 edges of minimum total cost:

1. Sort edges by cost.
2. Take each edge whose ends are in different groups (unite them).
3. If you took fewer than n − 1 edges, the graph is disconnected ([Road Reparation](https://cses.fi/problemset/task/1675): IMPOSSIBLE).

For dense graphs (every pair of points), Prim's O(n²) version without a heap is simpler and faster.

### Practice (Lecture 25)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Road Reparation](https://cses.fi/problemset/task/1675) | In-class | Medium | Section 2 |
| [Road Construction](https://cses.fi/problemset/task/1676) | In-class | Medium | Section 1 |
| [Redundant Connection](https://leetcode.com/problems/redundant-connection/) | Take-home | Medium | First edge whose ends are already connected |
| [Accounts Merge](https://leetcode.com/problems/accounts-merge/) | Take-home | Medium | Unite e-mails that share an account |
| [Min Cost to Connect All Points](https://leetcode.com/problems/min-cost-to-connect-all-points/) | Take-home | Medium | Prim O(n²) |
| [News Distribution](https://codeforces.com/problemset/problem/1167/C) | Take-home | Medium | Answer = size of each user's group |
| [Roads not only in Berland](https://codeforces.com/problemset/problem/25/D) | Take-home | Medium | Collect redundant roads, then use them to link components |
| [Make It Connected](https://codeforces.com/problemset/problem/1095/F) | Take-home | Hard | Add edges from the cheapest node to all others, plus the offers |

### Quiz (Lectures 24–25)

1. Why can't Dijkstra handle negative edges?
2. In Floyd–Warshall, which loop is outermost?
3. How does Bellman–Ford detect a negative cycle?
4. What two tricks make DSU fast?
5. When does Kruskal add an edge?

## Lecture 26: SCC, bridges & articulation points

### 1. Strongly connected components

In a directed graph, an SCC is a largest group where every node can reach every other. **Kosaraju's algorithm:**

1. DFS the graph; record nodes in the order they finish.
2. Reverse every edge.
3. Go through nodes in reverse finish order; each DFS on the reversed graph from an unassigned node collects exactly one SCC.

Shrinking each SCC to one node gives a DAG (the **condensation**), so you can run DAG DP on it ([Coin Collector](https://cses.fi/problemset/task/1686)).

Quick check, one SCC or not ([Flight Routes Check](https://cses.fi/problemset/task/1682)): BFS from node 1 in the graph and in the reversed graph. If both reach everything, the whole graph is one SCC; otherwise print a pair that fails.

### 2. Bridges and articulation points

In an undirected graph, a **bridge** is an edge whose removal disconnects the graph; an **articulation point** is such a vertex.

During DFS record tin\[v\] (entry time) and low\[v\] = the smallest tin reachable from v's subtree using at most one back edge.

- Edge (p, c) is a bridge if low\[c\] > tin\[p\].
- Vertex p (not the root) is an articulation point if some child has low\[c\] ≥ tin\[p\]. The root is one if it has two or more DFS children.

Skip only the exact edge you arrived by (use edge ids), so parallel edges are handled correctly.

### 3. Deep recursion

These algorithms recurse. For 10^5 nodes, write them iteratively, or in Java run `solve()` inside `new Thread(null, runnable, "main", 1 << 27)`.

### Practice (Lecture 26)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Flight Routes Check](https://cses.fi/problemset/task/1682) | In-class | Medium | Section 1, quick check |
| [Planets and Kingdoms](https://cses.fi/problemset/task/1683) | In-class | Medium | Kosaraju; label each SCC |
| [Checkposts](https://codeforces.com/problemset/problem/427/C) | Take-home | Medium | Per SCC: cheapest cost and how many nodes have it |
| [Bertown roads](https://codeforces.com/problemset/problem/118/E) | Take-home | Hard | Any bridge → 0; otherwise orient edges by DFS |
| [Critical Connections](https://leetcode.com/problems/critical-connections-in-a-network/) | Take-home | Hard | List all bridges |
| [Coin Collector](https://cses.fi/problemset/task/1686) | Take-home | Hard | Sum coins per SCC, then longest path on the condensation |

## Lecture 27: Graph lab + Contest 2

### 1. Name the algorithm

| If the problem has… | Think… |
| --- | --- |
| A grid, minimum steps | BFS |
| “Minimise the largest edge on the path” | Dijkstra on max, or binary search + BFS, or DSU by weight |
| Dependencies, “valid order” | Topological sort |
| Connect everything cheaply | MST |
| Groups that merge over time | DSU |
| Each node has exactly one outgoing edge, “where after k steps?” | Binary lifting on the successor |
| Use every edge exactly once | Euler path (degrees + Hierholzer) |

### 2. Contest 2

90 minutes, 4 graph problems you haven't seen in class. Same rules as before. Upsolve within 48 hours.

### Practice (Lecture 27)

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Message Route](https://cses.fi/problemset/task/1667) | In-class | Easy | BFS with parents |
| [Path With Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/) | In-class | Medium | Dijkstra where path cost = largest step |
| [Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/) | Take-home | Hard | Same idea as Minimum Effort |
| [Moving to the Capital](https://codeforces.com/problemset/problem/1472/G) | Take-home | Hard | BFS distances, then DP from far to near |
| [Planets Queries I](https://cses.fi/problemset/task/1750) | Take-home | Hard | Binary lifting, 30 levels for k ≤ 10^9 |
| [Mail Delivery](https://cses.fi/problemset/task/1691) | Take-home | Hard | All degrees even + connected → Hierholzer |

### Quiz (Lectures 26–27)

1. Describe Kosaraju's two passes.
2. When is edge (p, c) a bridge?
3. Why is the condensation of SCCs always a DAG?
4. Which algorithm for “minimise the largest edge on a path”?
5. When does an undirected graph have an Euler circuit?
