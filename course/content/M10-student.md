# M10 Strings: Student Handbook

Nov 27, 2026 · @Anoop

## Lecture 36: String algorithms

Checking a pattern at every position of a text is O(n · m). These tools do it in O(n + m).

### 1. Pick the tool

| Task | Tool |
| --- | --- |
| Find all occurrences of a pattern | Prefix function (KMP) or Z-function |
| Borders, periods of a string | Prefix function / Z-function |
| Compare any two substrings quickly | Rolling hash |
| Many words, prefix lookups, autocomplete | Trie |
| Longest palindrome | Expand around centre (O(n²)) or Manacher (O(n)) |

### 2. Prefix function

π\[i\] = length of the longest proper prefix of s\[0..i\] that is also a suffix of it.

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| s | a | a | b | a | a | a | b |
| π | 0 | 1 | 0 | 1 | 2 | 2 | 3 |

```cpp
vector<int> prefixFunction(const string& s) {
    int n = s.size(); vector<int> pi(n, 0);
    for (int i = 1; i < n; i++) {
        int k = pi[i-1];
        while (k > 0 && s[i] != s[k]) k = pi[k-1];
        if (s[i] == s[k]) k++;
        pi[i] = k;
    }
    return pi;
}
```

```java
static int[] prefixFunction(String s) {
    int n = s.length(); int[] pi = new int[n];
    for (int i = 1; i < n; i++) {
        int k = pi[i - 1];
        while (k > 0 && s.charAt(i) != s.charAt(k)) k = pi[k - 1];
        if (s.charAt(i) == s.charAt(k)) k++;
        pi[i] = k;
    }
    return pi;
}
```

**Counting occurrences** ([String Matching](https://cses.fi/problemset/task/1753)): compute π of pattern + '#' + text; every position where π equals the pattern length is a match.

**All borders** ([Finding Borders](https://cses.fi/problemset/task/1732)): start with k = π\[n−1\] and follow k = π\[k−1\] until 0.

### 3. Z-function

z\[i\] = length of the longest common prefix of s and the suffix starting at i. p is a period of s exactly when z\[p\] = n − p (and p = n always works). ([Finding Periods](https://cses.fi/problemset/task/1733))

### 4. Rolling hash

Treat a string as a number in base B modulo a big prime M. With prefix hashes h and powers pw, the hash of s\[l..r) is (h\[r\] − h\[l\] · pw\[r − l\]) mod M. Two equal substrings always have equal hashes; unequal ones collide rarely. Use a random base, and two different moduli when it matters.

### 5. Trie

A tree where each edge is a letter and each root-to-node path is a prefix. Insert and search cost O(word length). Store children as an array of 26.

```cpp
struct Trie {
    vector<array<int, 26>> nxt{{}}; vector<bool> end{false};
    void insert(const string& w) { int v = 0;
        for (char ch : w) { int c = ch - 'a';
            if (!nxt[v][c]) { nxt[v][c] = nxt.size(); nxt.push_back({}); end.push_back(false); }
            v = nxt[v][c]; }
        end[v] = true; }
};
```

```java
static int[][] nxt = new int[1_000_001][26]; static boolean[] end = new boolean[1_000_001]; static int cnt = 1;
static void insert(String w) { int v = 0;
    for (int i = 0; i < w.length(); i++) { int c = w.charAt(i) - 'a';
        if (nxt[v][c] == 0) nxt[v][c] = cnt++;
        v = nxt[v][c]; }
    end[v] = true; }
```

Size the Java arrays to the total length of all words plus one.

**Word Combinations** ([CSES 1731](https://cses.fi/problemset/task/1731)): dp\[i\] = ways to build the suffix starting at i. From each i, walk the trie along s\[i..\]; whenever you hit a word end at j, add dp\[j + 1\].

### 6. Palindromes

Expand around each centre (n odd centres, n − 1 even ones): O(n²), fine for n ≤ 1000 ([LeetCode 5](https://leetcode.com/problems/longest-palindromic-substring/)). For n = 10^6 use Manacher's algorithm ([CSES 1111](https://cses.fi/problemset/task/1111)).

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [String Matching](https://cses.fi/problemset/task/1753) | In-class | Easy | Section 2 |
| [Finding Borders](https://cses.fi/problemset/task/1732) | In-class | Medium | Section 2 |
| [Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/) | In-class | Medium | Section 5 |
| [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) | Take-home | Medium | Section 6 |
| [Finding Periods](https://cses.fi/problemset/task/1733) | Take-home | Medium | Section 3 |
| [Good Substrings](https://codeforces.com/problemset/problem/271/D) | Take-home | Medium | Insert every good substring into a trie; count nodes |
| [Password](https://codeforces.com/problemset/problem/126/B) | Take-home | Hard | A border that also appears strictly inside the string |
| [Word Combinations](https://cses.fi/problemset/task/1731) | Take-home | Hard | Section 5 |
| [Word Search II](https://leetcode.com/problems/word-search-ii/) | Take-home | Hard | Trie of words + grid DFS |
| [Longest Palindrome](https://cses.fi/problemset/task/1111) | Take-home | Hard | Manacher |
| [Compress Words](https://codeforces.com/problemset/problem/1200/E) | Take-home | Hard | Overlap via prefix function on next + '#' + end of result |

### Quiz

1. What does π\[i\] store?
2. How do you count pattern occurrences with the prefix function?
3. What does z\[i\] mean?
4. Why use a random base or two moduli for hashing?
5. What is the cost of inserting a word into a trie?
