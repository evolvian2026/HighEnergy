# M11 Placement Readiness: Student Handbook

The last four lectures turn your DSA skill into offers: online assessments, design rounds, interviews and your resume.

## Lecture 37: Online assessments

### 1. What to expect

Usually 2–3 problems in 60–90 minutes on a HackerRank- or HackerEarth-style platform. Hidden tests, partial credit for tests passed, often no autocomplete, sometimes webcam proctoring.

### 2. OA playbook

1. **Read everything first** (5 minutes). Rank problems by how sure you are.
2. **Bank points early:** solve the one you're surest of first.
3. **No idea in 10 minutes?** Submit a correct brute force for partial credit, then improve it.
4. **Test before submitting:** n = 1, duplicates, negatives, largest sizes, empty input.
5. **Watch the clock:** an untouched problem is worth more than polishing a solved one.

### 3. Which module does this question come from?

| If you see… | Think | Module |
| --- | --- | --- |
| “number of subarrays with sum/property…” | Prefix sums + hashing | M1 |
| “longest substring/subarray such that…” | Sliding window | M1 |
| “minimum capacity / speed / days to…” | Binary search on the answer | M2 |
| “schedule / rooms / k largest…” | Heap greedy | M4 |
| “islands, maze, groups, connections…” | BFS / DSU | M7 |
| “number of ways / minimum cost to reach…” | DP | M8 |

### OA practice set

| Problem | Level | Pattern |
| --- | --- | --- |
| [3Sum](https://leetcode.com/problems/3sum/) | Medium | Sort + two pointers, skip duplicates |
| [Next Permutation](https://leetcode.com/problems/next-permutation/) | Medium | Find the pivot, swap, reverse the suffix |
| [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) | Medium | Backtracking with open/close counts |
| [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) | Medium | Map + binary search on timestamps |
| [Design Twitter](https://leetcode.com/problems/design-twitter/) | Medium | Heap merge of followed users' feeds |
| [Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) | Hard | Histogram per row (Lecture 12) |
| [Sliding Window Median](https://leetcode.com/problems/sliding-window-median/) | Hard | Two heaps with lazy deletion (Lecture 13) |
| [The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/) | Hard | Sweep line + max-heap or multiset |

## Lecture 38: Low-level design

### 1. What interviewers check

Can you turn a vague request (“design a parking lot”) into clean classes with clear responsibilities, and explain trade-offs?

### 2. The five-step answer

1. Clarify requirements and what's out of scope.
2. List entities and what each is responsible for.
3. Draw relationships: has-a (composition) before is-a (inheritance).
4. Define the main methods and the data structures behind them.
5. Discuss extension, concurrency (two users, one resource) and failure cases.

### 3. SOLID in one line each

| Principle | Meaning |
| --- | --- |
| Single responsibility | A class has one reason to change |
| Open/closed | Add behaviour by adding code, not editing old code |
| Liskov substitution | A subclass must work wherever its parent does |
| Interface segregation | Small, focused interfaces |
| Dependency inversion | Depend on interfaces, not concrete classes |

### 4. Patterns you should recognise

- **Strategy:** swap an algorithm at runtime (LRU vs LFU eviction in Project 1)
- **Observer:** notify subscribers when something changes
- **Factory:** create the right object type from input (Car, Bike, Truck)
- **Singleton:** exactly one shared instance (configuration); use sparingly

### Design coding practice

| Problem | Level | Hint |
| --- | --- | --- |
| [Design Browser History](https://leetcode.com/problems/design-browser-history/) | Medium | Array with a current index; visiting truncates forward history |
| [Design Underground System](https://leetcode.com/problems/design-underground-system/) | Medium | Map of check-ins + map of (from, to) → total time and count |
| [Snapshot Array](https://leetcode.com/problems/snapshot-array/) | Medium | Per index, list of (snapId, value); binary search on get |
| [Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/) | Easy | Two stacks; move only when the output stack is empty |

## Lecture 39: Interviews, resume & profile

### 1. Think aloud: the 7 steps

1. Restate the problem; ask about constraints and edge cases.
2. Work a small example by hand.
3. Give a brute force and its complexity.
4. Improve it and name the pattern.
5. Code cleanly while explaining.
6. Dry-run your code; test edge cases.
7. State the final time and space complexity.

### 2. How you'll be scored

| Criterion | Weight | What a 5 looks like |
| --- | --- | --- |
| Problem understanding | 15% | Clarifies constraints and edge cases before coding |
| Approach | 30% | Reaches the optimal idea alone and compares options |
| Coding | 25% | Clean, correct, good names |
| Testing & complexity | 15% | Tests edge cases and states exact complexity |
| Communication | 15% | Thinks aloud the whole time |

### 3. Behavioural answers (STAR)

Situation, Task, Action, Result. Prepare five stories: a conflict, a failure, leading something, a tight deadline, and a project deep-dive (your capstone works well).

### 4. Resume checklist

- [ ] One page
- [ ] GitHub, LinkedIn, Codeforces and LeetCode links with current ratings
- [ ] 2–3 projects: what it does, the DSA inside, one measurable result
- [ ] Contest ranks and problems solved
- [ ] Only skills you can talk about for 5 minutes

### Interview practice set

| Problem | Level | Hint |
| --- | --- | --- |
| [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | Track the minimum so far |
| [Group Anagrams](https://leetcode.com/problems/group-anagrams/) | Medium | Key = sorted word or letter counts |
| [Rotate Image](https://leetcode.com/problems/rotate-image/) | Medium | Transpose, then reverse each row |
| [Spiral Matrix](https://leetcode.com/problems/spiral-matrix/) | Medium | Shrink four boundaries |
| [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) | Medium | Use row 0 and column 0 as markers |
| [Search a 2D Matrix](https://leetcode.com/problems/search-a-2d-matrix/) | Medium | Binary search on the flattened index |
| [Decode String](https://leetcode.com/problems/decode-string/) | Medium | Stack of (count, string so far) |
| [Asteroid Collision](https://leetcode.com/problems/asteroid-collision/) | Medium | Stack simulation |
| [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) | Medium | Greedy by end time (Lecture 6) |
| [Minimum Number of Arrows](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) | Medium | Greedy by end time |

## Lecture 40: Final contest & capstone

### Final contest (2 hours, 5 problems)

| Problem | Level | Hint after the contest |
| --- | --- | --- |
| [Josephus Problem I](https://cses.fi/problemset/task/2162) | Medium | Queue simulation |
| [Playlist](https://cses.fi/problemset/task/1141) | Medium | Sliding window with last-seen positions |
| [Movie Festival II](https://cses.fi/problemset/task/1632) | Hard | Sort by end; multiset of members' free times |
| [Increasing Subsequence II](https://cses.fi/problemset/task/1748) | Hard | Compress values; BIT of counts |
| [Distinct Values Queries](https://cses.fi/problemset/task/1734) | Hard | Offline by right end; BIT keeps only last occurrences |

### Capstone demo (6–8 minutes per team)

Show search, autocomplete, spell correction and the analytics view live. Be ready to explain the complexity of each feature and one design decision you would change.

### Your plan after the course

- One rated contest every week (Codeforces, CodeChef Starters, LeetCode or AtCoder)
- Redo every problem marked “Revisit” in the portal
- One mock OA every three days in the two weeks before placement drives
- Keep your resume and coding profiles updated after every contest
