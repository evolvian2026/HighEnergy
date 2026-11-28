# M0 Foundations & CP Setup: Student Handbook

Nov 27, 2026 · @Anoop

## Start here

Module 0 sets up your tools and habits for the whole course: reading constraints, choosing a complexity, using the standard library, and testing your own code. It runs over Lectures 1 and 2.

### Setup checklist (finish before Lecture 1)

- [ ] Create accounts on [Codeforces](https://codeforces.com), [CSES](https://cses.fi/problemset/), [LeetCode](https://leetcode.com) and [AtCoder](https://atcoder.jp)
- [ ] Install a compiler: g++ 11+ (C++17) or JDK 17+
- [ ] Install an editor (VS Code with the C++ or Java extension)
- [ ] Open the course portal at dsa.evolvian.in and fill in your profile
- [ ] Create a GitHub repo called `dsa-solutions` for your accepted code

### The course template

Start every problem from this template. It reads input fast and handles several test cases.

```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

void solve() {
    // read input, solve, print
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int t = 1;
    // cin >> t;   // uncomment when the problem has many test cases
    while (t--) solve();
}
```

```java
import java.io.*;
import java.util.*;

public class Main {
    static BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    static StringTokenizer st;
    static PrintWriter out = new PrintWriter(new BufferedOutputStream(System.out));

    static String next() throws IOException {
        while (st == null || !st.hasMoreTokens()) st = new StringTokenizer(br.readLine());
        return st.nextToken();
    }
    static int nextInt() throws IOException { return Integer.parseInt(next()); }
    static long nextLong() throws IOException { return Long.parseLong(next()); }

    static void solve() throws IOException {
        // read input, solve, print with out.println(...)
    }

    public static void main(String[] args) throws IOException {
        int t = 1;
        // t = nextInt();
        while (t-- > 0) solve();
        out.flush();
    }
}
```

Java tip: keep the class name `Main` and don't add a `package` line. That works on every judge used in this course.

## Lecture 1: Complexity & the CP environment

By the end of this lecture you can look at a problem's limits and know how fast your solution must be, and you have two accepted submissions on CSES.

### 1. Why constraints come first

A computer does roughly **10^8 simple operations per second**. Most problems give a 1–2 second time limit. So the input size tells you which algorithms can work before you read the story.

| n up to | Your solution must be about | Typical idea |
| --- | --- | --- |
| 10 | O(n!) | Try every permutation |
| 20 | O(2^n) | Try every subset |
| 500 | O(n^3) | Three nested loops |
| 5,000 | O(n^2) | Two nested loops |
| 10^5 – 10^6 | O(n log n) or O(n) | Sorting, binary search, one pass |
| 10^9+ | O(log n) or O(1) | A formula or repeated halving |

**Worked check.** n = 2 × 10^5. A double loop does about (2 × 10^5)^2 = 4 × 10^10 steps: 400 seconds. Too slow. Sorting does about n log n ≈ 3.5 × 10^6 steps: fine.

### 2. Big-O in one minute

Big-O counts how the work grows as n grows, ignoring constant factors.

- One loop over n items: O(n)
- A loop inside a loop: O(n^2)
- Halving the range each step (binary search): O(log n)
- Sorting: O(n log n)

### 3. Judge verdicts

| Verdict | Meaning | Usual cause |
| --- | --- | --- |
| AC | Accepted | Correct and fast enough |
| WA | Wrong Answer | Logic bug, overflow, missed edge case, wrong output format |
| TLE | Time Limit Exceeded | Algorithm too slow, slow I/O, infinite loop |
| RE | Runtime Error | Array out of bounds, division by zero, stack overflow |
| MLE | Memory Limit Exceeded | Arrays too large, storing too much |

### 4. Overflow: the silent killer

A 32-bit `int` holds values up to about **2.1 × 10^9**. Beyond that it wraps around to negative numbers without any error.

```cpp
int a = 100000, b = 100000;
long long bad  = a * b;            // multiplies as int first: overflow
long long good = 1LL * a * b;      // 10,000,000,000: correct
```

```java
int a = 100000, b = 100000;
long bad  = a * b;                 // overflow before widening
long good = (long) a * b;          // correct
```

Rule: if values or sums can pass 2 × 10^9, use `long long` (C++) or `long` (Java).

### 5. Worked example: Weird Algorithm

[CSES 1068](https://cses.fi/problemset/task/1068). Start from n. If n is even, divide by 2; if odd, multiply by 3 and add 1. Print every value until you reach 1.

**Think first.** n ≤ 10^6, but 3n + 1 can grow far beyond that. Values pass 2 × 10^9, so use a 64-bit type.

```cpp
long long n; cin >> n;
while (true) {
    cout << n << ' ';
    if (n == 1) break;
    n = (n % 2 == 0) ? n / 2 : 3 * n + 1;
}
```

```java
long n = nextLong();
StringBuilder sb = new StringBuilder();
while (true) {
    sb.append(n).append(' ');
    if (n == 1) break;
    n = (n % 2 == 0) ? n / 2 : 3 * n + 1;
}
out.println(sb);
```

### 6. Worked example: Missing Number

[CSES 1083](https://cses.fi/problemset/task/1083). You get n − 1 distinct numbers from 1..n. Find the missing one.

**Idea.** The numbers 1..n sum to n(n + 1)/2. Subtract what you read. Dry run with n = 5 and input 2 3 1 5: expected 15, actual 11, missing 4.

**Alternative.** XOR all of 1..n and all inputs. Equal numbers cancel (x XOR x = 0), leaving the missing one. No overflow possible.

Time O(n), memory O(1).

### 7. Common mistakes

- Using `int` for sums or products that can exceed 2 × 10^9
- C++: using `endl` instead of `'\n'` (very slow on big outputs)
- Java: using `Scanner` and `System.out.println` in loops (TLE on large input)
- Leaving debug prints in your submission
- Testing only the sample input

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Weird Algorithm](https://cses.fi/problemset/task/1068) | In-class | Easy | Worked above |
| [Missing Number](https://cses.fi/problemset/task/1083) | In-class | Easy | Worked above |
| [Increasing Array](https://cses.fi/problemset/task/1094) | Take-home | Easy | Each element must be at least the one before it. Count how much you raise it |
| [Number Spiral](https://cses.fi/problemset/task/1071) | Take-home | Medium | Look at the layer max(row, col). Find a formula; don't build the grid |
| [Watermelon](https://codeforces.com/problemset/problem/4/A) | Take-home | Easy | Two even, positive parts. Check small values carefully |

### Quiz

1. n ≤ 10^5. Which complexities are safe: O(n^2), O(n log n), O(n)?
2. What verdict does an infinite loop usually give?
3. What is the largest value a 32-bit signed int can hold, roughly?
4. Why is `endl` slow in C++?
5. Missing Number with n = 5 and input 1 2 4 5. What is the answer, and how did you get it?

## Lecture 2: Standard library toolkit, sorting & comparators

By the end of this lecture you can pick the right container for a task, sort anything with a custom rule, and catch your own bugs with a stress tester.

### 1. Pick the container by the operations you need

| You need to… | C++ | Java | Cost per operation |
| --- | --- | --- | --- |
| Store items in order, access by index | `vector` | `ArrayList` or array | O(1) |
| Check “have I seen x?” | `unordered_set` | `HashSet` | O(1) average |
| Count occurrences | `unordered_map` | `HashMap` | O(1) average |
| Keep keys sorted; find “smallest ≥ x” | `set` / `map` | `TreeSet` / `TreeMap` | O(log n) |
| Sorted with duplicates | `multiset` | `TreeMap<value, count>` | O(log n) |
| Repeatedly take the min or max | `priority_queue` | `PriorityQueue` | O(log n) |
| Add/remove at both ends | `deque` | `ArrayDeque` | O(1) |

**Hash vs ordered.** Hash containers are faster on average but give no order, and special tests on Codeforces can make them slow. Ordered containers are O(log n) and always safe.

### 2. Sorting with your own rule

Sort intervals by end time, and by start time when ends are equal:

```cpp
vector<pair<int,int>> v;   // {start, end}
sort(v.begin(), v.end(), [](const auto& a, const auto& b) {
    if (a.second != b.second) return a.second < b.second;
    return a.first < b.first;
});
```

```java
int[][] v = new int[n][2];   // {start, end}
Arrays.sort(v, (a, b) -> a[1] != b[1]
        ? Integer.compare(a[1], b[1])
        : Integer.compare(a[0], b[0]));
```

Rules for comparators:

- Use `<` (strict), never `<=`. A comparator that says a < a breaks sorting.
- Don't write `return a - b;`. It overflows for large values. Use `Integer.compare(a, b)` in Java.
- Java: `Arrays.sort` on a primitive `int[]` can be slowed to O(n^2) by crafted tests. Shuffle the array first, or sort an `Integer[]` or a `List`.

### 3. Worked example: Distinct Numbers

[CSES 1621](https://cses.fi/problemset/task/1621). Count distinct values among n numbers (n ≤ 2 × 10^5).

**Way 1: sort and count changes.** After sorting, equal values sit together. Count positions where a\[i\] differs from a\[i−1\], plus one. O(n log n).

**Way 2: hash set.** Insert everything; print the size. O(n) average.

```cpp
sort(a.begin(), a.end());
int cnt = 1;
for (int i = 1; i < n; i++) if (a[i] != a[i-1]) cnt++;
cout << cnt << '\n';
```

```java
List<Integer> a = new ArrayList<>();   // a List sorts with merge sort: no slow worst case
for (int i = 0; i < n; i++) a.add(nextInt());
Collections.sort(a);
int cnt = 1;
for (int i = 1; i < n; i++) if (!a.get(i).equals(a.get(i - 1))) cnt++;
out.println(cnt);
```

### 4. Worked example: Concert Tickets

[CSES 1091](https://cses.fi/problemset/task/1091). n tickets with prices; m customers arrive one by one, each with a maximum price t. Each buys the most expensive ticket that costs at most t, or gets −1.

**What we need.** “Find the largest price ≤ t” and “remove one ticket”, both fast, with duplicate prices. That is an ordered multiset.

**Dry run.** Prices {5, 3, 7, 8, 5}; customers 4, 8, 3.

| Customer t | Largest price ≤ t | Remaining tickets |
| --- | --- | --- |
| 4 | 3 | 5, 5, 7, 8 |
| 8 | 8 | 5, 5, 7 |
| 3 | none → −1 | 5, 5, 7 |

```cpp
multiset<int> s(prices.begin(), prices.end());
for (int t : customers) {
    auto it = s.upper_bound(t);         // first price greater than t
    if (it == s.begin()) { cout << -1 << '\n'; continue; }
    --it;                                // step back: largest price <= t
    cout << *it << '\n';
    s.erase(it);                         // removes ONE ticket
}
```

```java
TreeMap<Integer, Integer> m = new TreeMap<>();   // price -> count
for (int p : prices) m.merge(p, 1, Integer::sum);
for (int t : customers) {
    Integer k = m.floorKey(t);           // largest price <= t
    if (k == null) { out.println(-1); continue; }
    out.println(k);
    if (m.merge(k, -1, Integer::sum) == 0) m.remove(k);
}
```

Time O((n + m) log n).

### 5. Stress testing your code

When your solution fails a hidden test, compare it against a slow but obviously correct version on thousands of small random inputs.

1. `gen`: prints a random small test (for example n between 1 and 8, values 1..10).
2. `brute`: the simplest correct solution, however slow.
3. `sol`: your fast solution.
4. A loop that runs `gen`, feeds the test to both, and stops at the first different output.

```bash
for i in $(seq 1 1000); do
  ./gen $i > in.txt
  ./brute < in.txt > b.txt
  ./sol   < in.txt > s.txt
  if ! cmp -s b.txt s.txt; then echo "Mismatch on test $i"; cat in.txt; break; fi
done
```

This is exactly what you build in **Project 0** (due Lecture 4).

### 6. Common mistakes

- C++: `s.erase(x)` on a multiset deletes **all** copies of x. Erase an iterator instead.
- C++: `std::lower_bound(s.begin(), s.end(), x)` on a set is slow (O(n)). Use `s.lower_bound(x)`.
- Java: comparing two `Integer` objects with `==`. It fails for values above 127. Use `.equals()`.
- Java: forgetting to remove a key from a TreeMap multiset when its count reaches 0.

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Distinct Numbers](https://cses.fi/problemset/task/1621) | In-class | Easy | Worked above |
| [Concert Tickets](https://cses.fi/problemset/task/1091) | In-class | Medium | Worked above |
| [Apartments](https://cses.fi/problemset/task/1084) | Take-home | Easy | Sort both lists. Walk through them together with two pointers |
| [Ferris Wheel](https://cses.fi/problemset/task/1090) | Take-home | Easy | Sort. Try to pair the heaviest child with the lightest one |
| [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) | Take-home | Medium | Count first. Then keep only the k best with a small heap |

### Quiz

1. You need “smallest element ≥ x” while inserting and deleting. Which container?
2. Why is `return a - b;` a risky comparator?
3. In C++, what does `multiset.erase(5)` do if the multiset holds three 5s?
4. Why shuffle an `int[]` before `Arrays.sort` in Java?
5. Name the three programs a stress tester needs.
