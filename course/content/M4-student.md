# M4 Linear Data Structures: Student Handbook

Nov 27, 2026 · @Anoop

Stacks, deques, heaps and linked lists appear in almost every interview loop. This module teaches the patterns, not just the containers.

## Lecture 12: Stacks & monotonic stack

A monotonic stack finds, for every position, the nearest smaller (or greater) element in O(n) total.

### 1. Stack basics

Last in, first out. Classic use: matching brackets. Push openers; on a closer, the top must be its partner. C++: `vector` or `stack`. Java: `ArrayDeque` (not the old `Stack` class), or a plain array with a top index.

### 2. The monotonic stack idea

To find the nearest smaller value to the **left** of each a\[i\]: keep a stack of indices whose values increase from bottom to top. Before pushing i, pop every index whose value is ≥ a\[i\]. They can never be anyone's answer again, because a\[i\] is both closer and smaller. Whatever remains on top is the answer.

Each index is pushed once and popped at most once, so the total work is O(n).

### 3. Worked example: Nearest Smaller Values

[CSES 1645](https://cses.fi/problemset/task/1645). For each position print the nearest position to its left with a smaller value (1-based), or 0.

**Dry run.** a = \[2, 5, 1, 4, 8, 3, 2, 5\] gives 0 1 0 3 4 3 3 7.

```cpp
vector<int> st;                          // indices; values increase upwards
for (int i = 0; i < n; i++) {
    while (!st.empty() && a[st.back()] >= a[i]) st.pop_back();
    cout << (st.empty() ? 0 : st.back() + 1) << ' ';
    st.push_back(i);
}
```

```java
int[] st = new int[n]; int top = 0;
StringBuilder sb = new StringBuilder();
for (int i = 0; i < n; i++) {
    while (top > 0 && a[st[top - 1]] >= a[i]) top--;
    sb.append(top == 0 ? 0 : st[top - 1] + 1).append(' ');
    st[top++] = i;
}
out.println(sb);
```

### 4. Worked example: Largest Rectangle in Histogram

[LeetCode 84](https://leetcode.com/problems/largest-rectangle-in-histogram/). Bars of width 1 and given heights. Largest rectangle?

**Key idea.** In the best rectangle, some bar is the shortest. For each bar, stretch left and right until a shorter bar: width = nextSmaller − prevSmaller − 1. One monotonic stack pass finds both limits when a bar is popped.

**Dry run.** heights = \[2, 1, 5, 6, 2, 3\]. Bar 5 (index 2) stretches over indices 2..3: area 5 × 2 = 10. That is the answer.

```cpp
int largestRectangleArea(vector<int>& h) {
    vector<int> st; long long best = 0; int n = h.size();
    for (int i = 0; i <= n; i++) {
        int cur = (i == n) ? 0 : h[i];                    // height-0 sentinel flushes the stack
        while (!st.empty() && h[st.back()] > cur) {
            int height = h[st.back()]; st.pop_back();
            int left = st.empty() ? -1 : st.back();
            best = max(best, 1LL * height * (i - left - 1));
        }
        st.push_back(i);
    }
    return (int)best;
}
```

```java
public int largestRectangleArea(int[] h) {
    int n = h.length; int[] st = new int[n + 1]; int top = 0; long best = 0;
    for (int i = 0; i <= n; i++) {
        int cur = (i == n) ? 0 : h[i];
        while (top > 0 && h[st[top - 1]] > cur) {
            int height = h[st[--top]];
            int left = top == 0 ? -1 : st[top - 1];
            best = Math.max(best, (long) height * (i - left - 1));
        }
        st[top++] = i;
    }
    return (int) best;
}
```

### 5. The contribution technique

Ask “for each element, over which range is it the minimum (or maximum)?”. Previous/next smaller give that range in O(n). It solves window-minimum problems like Mike and Feet, and sums over all subarrays.

### 6. Common mistakes

- `if` instead of `while` when popping
- Storing values instead of indices
- Forgetting the final sentinel, so bars left on the stack are never measured
- Width off by one: it is right − left − 1

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Nearest Smaller Values](https://cses.fi/problemset/task/1645) | In-class | Easy | Worked above |
| [Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) | In-class | Hard | Worked above |
| [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/) | Take-home | Easy | Section 1 |
| [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) | Take-home | Medium | Next greater element; answer is the distance |
| [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) | Take-home | Hard | Water above i = min(max left, max right) − height |
| [Longest Regular Bracket Sequence](https://codeforces.com/problemset/problem/5/C) | Take-home | Hard | Stack of indices starting with −1 |
| [Mike and Feet](https://codeforces.com/problemset/problem/547/B) | Take-home | Hard | Section 5: each a\_i is the minimum of one maximal window |

### Quiz

1. Why is the monotonic stack O(n) even though it has a loop inside a loop?
2. Previous smaller (1-based) for a = \[3, 1, 2\]?
3. Write the width formula for the histogram rectangle of a popped bar.
4. Why add a bar of height 0 at the end?
5. In Mike and Feet, what should best\[L\] store?

## Lecture 13: Deques & heaps

A monotonic deque gives the maximum of every sliding window in O(n). A heap gives the smallest (or largest) item in O(log n), again and again.

### 1. Sliding window maximum with a deque

Keep indices in the deque with values **decreasing** from front to back.

1. Before adding i, pop from the back every index with value ≤ a\[i\] (they can never be a maximum again).
2. Push i at the back.
3. If the front index has left the window (≤ i − k), pop it from the front.
4. Once i ≥ k − 1, the front holds the window maximum.

**Dry run.** a = \[1, 3, −1, −3, 5, 3, 6, 7\], k = 3 gives maxima 3, 3, 5, 5, 6, 7.

```cpp
vector<int> maxSlidingWindow(vector<int>& a, int k) {
    deque<int> dq; vector<int> res;
    for (int i = 0; i < (int)a.size(); i++) {
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
        dq.push_back(i);
        if (dq.front() <= i - k) dq.pop_front();
        if (i >= k - 1) res.push_back(a[dq.front()]);
    }
    return res;
}
```

```java
public int[] maxSlidingWindow(int[] a, int k) {
    int n = a.length; int[] res = new int[n - k + 1];
    ArrayDeque<Integer> dq = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        while (!dq.isEmpty() && a[dq.peekLast()] <= a[i]) dq.pollLast();
        dq.addLast(i);
        if (dq.peekFirst() <= i - k) dq.pollFirst();
        if (i >= k - 1) res[i - k + 1] = a[dq.peekFirst()];
    }
    return res;
}
```

For the window **minimum** ([CSES 3221](https://cses.fi/problemset/task/3221)), flip the comparison to ≥. Read that problem's input and output format carefully before coding.

### 2. Heaps

|  | C++ | Java |
| --- | --- | --- |
| Default | `priority_queue<int>` is a **max**-heap | `PriorityQueue<Integer>` is a **min**-heap |
| Other way | `priority_queue<int, vector<int>, greater<int>>` | `new PriorityQueue<>(Collections.reverseOrder())` |
| Push / pop / top | `push`, `pop`, `top` | `add`, `poll`, `peek` |

All pushes and pops cost O(log n). A heap can't search for or delete an arbitrary item quickly.

### 3. Worked example: Kth Largest Element

[LeetCode 215](https://leetcode.com/problems/kth-largest-element-in-an-array/). Keep a min-heap of the k largest values seen so far. When it grows past k, drop its smallest. At the end, its top is the k-th largest. O(n log k).

```cpp
int findKthLargest(vector<int>& a, int k) {
    priority_queue<int, vector<int>, greater<int>> pq;
    for (int x : a) { pq.push(x); if ((int)pq.size() > k) pq.pop(); }
    return pq.top();
}
```

```java
public int findKthLargest(int[] a, int k) {
    PriorityQueue<Integer> pq = new PriorityQueue<>();
    for (int x : a) { pq.add(x); if (pq.size() > k) pq.poll(); }
    return pq.peek();
}
```

### 4. Two heaps for a running median

- `low`: a max-heap with the smaller half
- `high`: a min-heap with the larger half
- Keep size(low) equal to size(high) or one more
- Median = top of low (odd count), or the average of both tops (even count)

For a sliding window you must also delete the element that leaves. Heaps can't do that directly. Either mark it and skip it when it reaches the top (**lazy deletion**), or use ordered multisets instead (C++ `multiset`, Java `TreeMap` with counts).

### 5. Common mistakes

- Storing values instead of indices in the deque
- Using Java's `PriorityQueue.remove(x)`: it is O(n)
- Comparator `(a, b) -> b - a` overflowing for large numbers

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) | In-class | Hard | Worked above |
| [Sliding Window Minimum](https://cses.fi/problemset/task/3221) | In-class | Medium | Section 1 with the comparison flipped |
| [Kth Largest Element](https://leetcode.com/problems/kth-largest-element-in-an-array/) | In-class | Medium | Worked above |
| [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | Take-home | Hard | Section 4 |
| [Sliding Window Median](https://cses.fi/problemset/task/1076) | Take-home | Hard | Section 4 with deletions; for even k take the lower median |
| [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/) | Take-home | Hard | Heap of the current head of each list |
| [Smallest Range Covering K Lists](https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/) | Take-home | Hard | Heap of one element per list, plus the current maximum |

### Quiz

1. What does the front of the max-deque always hold?
2. What is the default heap in C++? In Java?
3. What is the complexity of Kth Largest with a size-k heap?
4. Why do we need lazy deletion for a sliding-window median?
5. Window maxima of \[1, 3, −1, −3, 5\] with k = 3?

## Lecture 14: Linked lists & data structure design

Interviewers love these: they test whether you can manage pointers without losing nodes, and combine structures to make every operation O(1).

### 1. Pointer discipline

- Draw the boxes and arrows first. Decide the order of rewiring so no node becomes unreachable.
- Use a **dummy head** node: the real head may change, the dummy never does.

Reverse a list iteratively:

```cpp
ListNode* reverse(ListNode* head) {
    ListNode* prev = nullptr;
    while (head) { ListNode* nxt = head->next; head->next = prev; prev = head; head = nxt; }
    return prev;
}
```

```java
ListNode reverse(ListNode head) {
    ListNode prev = null;
    while (head != null) { ListNode nxt = head.next; head.next = prev; prev = head; head = nxt; }
    return prev;
}
```

### 2. Floyd's cycle detection

Move `slow` one step and `fast` two steps. If there is a cycle they meet inside it. Then put one pointer back at the head and move both one step at a time: they meet at the **start of the cycle** ([LeetCode 142](https://leetcode.com/problems/linked-list-cycle-ii/)). O(n) time, O(1) memory.

### 3. Worked example: LRU Cache

[LeetCode 146](https://leetcode.com/problems/lru-cache/). get and put in O(1); when full, evict the least recently used key.

**Design.**

- A hash map finds a key's node in O(1).
- A doubly linked list keeps nodes in order of use: most recent at the front, least recent at the back. Moving or removing a node is O(1) when you hold a pointer to it.

**Trace with capacity 2.**

| Operation | List (front → back) | Result |
| --- | --- | --- |
| put(1, 1) | 1 |  |
| put(2, 2) | 2, 1 |  |
| get(1) | 1, 2 | 1 |
| put(3, 3) | 3, 1 | evicts 2 |
| get(2) | 3, 1 | −1 |

```cpp
class LRUCache {
    int cap;
    list<pair<int,int>> order;                                  // front = most recent
    unordered_map<int, list<pair<int,int>>::iterator> where;
public:
    LRUCache(int capacity) : cap(capacity) {}
    int get(int key) {
        auto it = where.find(key);
        if (it == where.end()) return -1;
        order.splice(order.begin(), order, it->second);         // move to front in O(1)
        return it->second->second;
    }
    void put(int key, int value) {
        auto it = where.find(key);
        if (it != where.end()) {
            it->second->second = value;
            order.splice(order.begin(), order, it->second);
            return;
        }
        if ((int)order.size() == cap) {                         // evict least recent
            where.erase(order.back().first);
            order.pop_back();
        }
        order.push_front({key, value});
        where[key] = order.begin();
    }
};
```

```java
class LRUCache {
    private static class Node { int key, val; Node prev, next; Node(int k, int v) { key = k; val = v; } }
    private final int cap;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0), tail = new Node(0, 0);   // sentinels

    public LRUCache(int capacity) { cap = capacity; head.next = tail; tail.prev = head; }
    private void unlink(Node x) { x.prev.next = x.next; x.next.prev = x.prev; }
    private void addFront(Node x) { x.next = head.next; x.prev = head; head.next.prev = x; head.next = x; }

    public int get(int key) {
        Node x = map.get(key);
        if (x == null) return -1;
        unlink(x); addFront(x);
        return x.val;
    }
    public void put(int key, int value) {
        Node x = map.get(key);
        if (x != null) { x.val = value; unlink(x); addFront(x); return; }
        if (map.size() == cap) { Node lru = tail.prev; unlink(lru); map.remove(lru.key); }
        x = new Node(key, value); addFront(x); map.put(key, x);
    }
}
```

This is the core of **Project 1**.

### 4. How to answer a design question in an interview

1. Clarify the operations and their limits (“do I need delete? what's the capacity?”).
2. State the invariant (“the list is ordered by last use”).
3. Pick structures that make each operation O(1) or O(log n).
4. Say the complexity, then code, then trace one example aloud.

### 5. Common mistakes

- Overwriting `next` before saving it
- Updating an existing key's value but forgetting to move it to the front
- Removing a node from the list but not from the map

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [LRU Cache](https://leetcode.com/problems/lru-cache/) | In-class | Medium | Worked above |
| [Reverse Nodes in k-Group](https://leetcode.com/problems/reverse-nodes-in-k-group/) | In-class | Hard | Dummy head; check k nodes exist, reverse them, reconnect |
| [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | Take-home | Medium | Map old → new, or weave copies between originals |
| [Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/) | Take-home | Medium | Section 2 |
| [Min Stack](https://leetcode.com/problems/min-stack/) | Take-home | Medium | Store the minimum-so-far with every element |
| [Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) | Take-home | Medium | Array + map to index; delete by swapping with the last element |
| [LFU Cache](https://leetcode.com/problems/lfu-cache/) | Take-home | Hard | One LRU list per frequency, plus the current minimum frequency |

### Quiz

1. Which two structures make LRU O(1)?
2. Why use a dummy head node?
3. In Floyd's algorithm, how do you find where the cycle starts?
4. LRU with capacity 2: put 1, put 2, get 1, put 3. Which key is evicted?
5. In GetRandom O(1), how do you delete an element in O(1)?
