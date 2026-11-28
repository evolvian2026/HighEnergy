# M5 Mathematics: Student Handbook

Nov 27, 2026 · @Anoop

The maths you need for placements and Codeforces up to about 1600: primes, modular arithmetic, counting, and fast recurrences.

## Lecture 15: Primes, GCD & sieves

### 1. Testing one number

Divisors come in pairs (d, n/d), and one of each pair is at most √n. So check divisors up to √n only: O(√n).

```cpp
bool isPrime(long long n) {
    if (n < 2) return false;
    for (long long d = 2; d * d <= n; d++) if (n % d == 0) return false;
    return true;
}
```

```java
static boolean isPrime(long n) {
    if (n < 2) return false;
    for (long d = 2; d * d <= n; d++) if (n % d == 0) return false;
    return true;
}
```

### 2. Sieve of Eratosthenes: all primes up to N

Mark multiples of each prime as composite, starting from p² (smaller multiples were already marked). O(N log log N), fast for N = 10^7.

**Smallest prime factor (SPF) sieve.** Store spf\[x\] instead of a yes/no. Then factorise any x ≤ N by dividing by spf\[x\] repeatedly: O(log x).

```cpp
const int N = 1000000; vector<int> spf(N + 1, 0);
for (int i = 2; i <= N; i++) if (spf[i] == 0)
    for (int j = i; j <= N; j += i) if (spf[j] == 0) spf[j] = i;
```

```java
int N = 1_000_000; int[] spf = new int[N + 1];
for (int i = 2; i <= N; i++) if (spf[i] == 0)
    for (int j = i; j <= N; j += i) if (spf[j] == 0) spf[j] = i;
```

### 3. Counting divisors

If n = p1^e1 · p2^e2 · … then the number of divisors is (e1 + 1)(e2 + 1)…

Example: 360 = 2³ · 3² · 5 has 4 · 3 · 2 = 24 divisors.

**Worked example: Counting Divisors** ([CSES 1713](https://cses.fi/problemset/task/1713)). Up to 10^5 numbers, each ≤ 10^6. Build the SPF sieve once, then:

```cpp
int x; cin >> x; int ans = 1;
while (x > 1) { int p = spf[x], e = 0; while (x % p == 0) { x /= p; e++; } ans *= (e + 1); }
cout << ans << '\n';
```

```java
int x = nextInt(), ans = 1;
while (x > 1) { int p = spf[x], e = 0; while (x % p == 0) { x /= p; e++; } ans *= (e + 1); }
out.println(ans);
```

### 4. Worked example: T-primes

[Codeforces 230B](https://codeforces.com/problemset/problem/230/B). A number has exactly three divisors only when it is p² for a prime p (divisors 1, p, p²). For x ≤ 10^12, sieve primes up to 10^6, take r = round(√x), and answer YES if r · r == x and r is prime.

Careful: floating-point √ can be off by one for big numbers. Round, then check r · r == x exactly.

### 5. GCD and LCM

- gcd(a, b) = gcd(b, a mod b), and gcd(a, 0) = a. C++ `std::gcd`, Java write it yourself (or `BigInteger.gcd`).
- lcm(a, b) = a / gcd(a, b) × b. Divide first to avoid overflow.
- gcd(u, v) = gcd(u − v, v). Useful when every number is shifted by the same amount (Row GCD).

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [T-primes](https://codeforces.com/problemset/problem/230/B) | In-class | Medium | Section 4 |
| [Counting Divisors](https://cses.fi/problemset/task/1713) | In-class | Easy | Section 3 |
| [Almost Prime](https://codeforces.com/problemset/problem/26/A) | Take-home | Easy | Count distinct prime factors for every number up to n |
| [Sherlock and his girlfriend](https://codeforces.com/problemset/problem/776/B) | Take-home | Easy | Primes one colour, composites another |
| [Common Divisors](https://cses.fi/problemset/task/1081) | Take-home | Medium | Try every d from large to small: how many values does d divide? |
| [Row GCD](https://codeforces.com/problemset/problem/1458/A) | Take-home | Medium | gcd(a1 + b, ai + b) = gcd(a1 + b, ai − a1) |

### Quiz

1. Why is it enough to test divisors up to √n?
2. What is the time complexity of the sieve of Eratosthenes?
3. How many divisors does 360 have?
4. How do you compute lcm(a, b) without overflow?
5. When does a number have exactly three divisors?

## Lecture 16: Modular arithmetic, fast power & nCr

Answers that would be astronomically large are asked “modulo 10^9 + 7”. You must keep every intermediate value reduced.

### 1. The rules

| Operation | Safe form (MOD = 10^9 + 7) |
| --- | --- |
| Add | (a + b) % MOD |
| Subtract | (a − b + MOD) % MOD |
| Multiply | (a × b) % MOD, with a and b in 64-bit |
| Divide by b | a × inverse(b) % MOD (MOD is prime) |

Two reduced values multiply to below 10^18, which fits in 64 bits. Three do not, so reduce after every product.

### 2. Fast power

Compute a^b in O(log b) by squaring: walk through the bits of b.

3^13: 13 = 1101 in binary, so 3^13 = 3^8 · 3^4 · 3^1.

```cpp
const long long MOD = 1000000007LL;
long long power(long long a, long long b, long long m = MOD) {
    long long r = 1; a %= m;
    while (b > 0) {
        if (b & 1) r = r * a % m;
        a = a * a % m;
        b >>= 1;
    }
    return r;
}
```

```java
static final long MOD = 1_000_000_007L;
static long power(long a, long b, long m) {
    long r = 1; a %= m;
    while (b > 0) {
        if ((b & 1) == 1) r = r * a % m;
        a = a * a % m;
        b >>= 1;
    }
    return r;
}
```

**Exponentiation II** ([CSES 1712](https://cses.fi/problemset/task/1712)) asks for a^(b^c). By Fermat's little theorem, exponents can be reduced modulo MOD − 1: answer = power(a, power(b, c, MOD − 1), MOD).

### 3. Modular inverse

For a prime p and x not divisible by p: inverse(x) = x^(p−2) mod p.

### 4. nCr for many queries

Precompute factorials and inverse factorials once, then each C(n, r) is O(1).

```cpp
const int MX = 1000000;
vector<long long> f(MX + 1), inv(MX + 1);
void build() {
    f[0] = 1; for (int i = 1; i <= MX; i++) f[i] = f[i-1] * i % MOD;
    inv[MX] = power(f[MX], MOD - 2);
    for (int i = MX; i > 0; i--) inv[i-1] = inv[i] * i % MOD;
}
long long C(int n, int r) { if (r < 0 || r > n) return 0; return f[n] * inv[r] % MOD * inv[n-r] % MOD; }
```

```java
static final int MX = 1_000_000;
static long[] f = new long[MX + 1], inv = new long[MX + 1];
static void build() {
    f[0] = 1; for (int i = 1; i <= MX; i++) f[i] = f[i - 1] * i % MOD;
    inv[MX] = power(f[MX], MOD - 2, MOD);
    for (int i = MX; i > 0; i--) inv[i - 1] = inv[i] * i % MOD;
}
static long C(int n, int r) { if (r < 0 || r > n) return 0; return f[n] * inv[r] % MOD * inv[n - r] % MOD; }
```

### 5. Stars and bars

Ways to give m identical items to n people (zero allowed) = C(n + m − 1, n − 1). Example: 5 apples, 3 children → C(7, 2) = 21.

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Exponentiation](https://cses.fi/problemset/task/1095) | In-class | Easy | Section 2 |
| [Exponentiation II](https://cses.fi/problemset/task/1712) | In-class | Medium | Section 2, last paragraph |
| [Binomial Coefficients](https://cses.fi/problemset/task/1079) | In-class | Medium | Section 4 |
| [Creating Strings II](https://cses.fi/problemset/task/1715) | Take-home | Medium | n! divided by the factorial of each letter's count |
| [Distributing Apples](https://cses.fi/problemset/task/1716) | Take-home | Medium | Section 5 |
| [Beautiful Numbers](https://codeforces.com/problemset/problem/300/C) | Take-home | Hard | Try every count i of digit a; check the digit sum; add C(n, i) |

### Quiz

1. Why is 10^9 + 7 the usual modulus?
2. How do you compute the inverse of x modulo a prime p?
3. In Exponentiation II, modulo what do you reduce b^c?
4. After precomputation, how long does each nCr query take?
5. How many ways are there to give 5 identical apples to 3 children?

## Lecture 17: Combinatorics, matrix exponentiation & games

### 1. Inclusion–exclusion

|A ∪ B| = |A| + |B| − |A ∩ B|. With more sets, add single sets, subtract pairs, add triples, and so on.

Numbers ≤ 20 divisible by 2 or 3: 10 + 6 − 3 = 13.

**Worked example: Prime Multiples** ([CSES 2185](https://cses.fi/problemset/task/2185)). Count numbers ≤ n divisible by at least one of k ≤ 20 primes. Loop over every non-empty mask of primes: multiply them (stop if the product passes n), then add n / product when the mask has an odd number of primes and subtract it when even.

```cpp
long long ans = 0;
for (int m = 1; m < (1 << k); m++) {
    long long prod = 1; bool over = false;
    for (int i = 0; i < k; i++) if (m >> i & 1) {
        if (prod > n / p[i]) { over = true; break; }
        prod *= p[i];
    }
    if (over) continue;
    ans += (__builtin_popcount(m) % 2 ? 1 : -1) * (n / prod);
}
```

```java
long ans = 0;
for (int m = 1; m < (1 << k); m++) {
    long prod = 1; boolean over = false;
    for (int i = 0; i < k; i++) if ((m >> i & 1) == 1) {
        if (prod > n / p[i]) { over = true; break; }
        prod *= p[i];
    }
    if (over) continue;
    ans += (Integer.bitCount(m) % 2 == 1 ? 1 : -1) * (n / prod);
}
```

### 2. Matrix exponentiation

A recurrence like F(n) = F(n−1) + F(n−2) is a matrix multiplication:

```latex
\begin{pmatrix} F(n+1) \\ F(n) \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} F(n) \\ F(n-1) \end{pmatrix}
```

So F(n) comes from the n-th power of that matrix, computed by fast power in O(log n) matrix products. This handles n up to 10^18 ([CSES 1722](https://cses.fi/problemset/task/1722)). A recurrence using the last k terms needs a k × k matrix: O(k³ log n).

### 3. Games

- A position is **losing** if every move leads to a winning position for the opponent.
- A position is **winning** if at least one move leads to a losing position.
- Fill a table from small positions upwards (Stick Game).
- **Nim:** with several piles, the first player wins exactly when the XOR of all pile sizes is not 0.

### 4. Derangements

Arrangements where nobody gets their own gift: D(1) = 0, D(2) = 1, D(n) = (n − 1)(D(n−1) + D(n−2)). D(4) = 9.

### Practice

| Problem | Type | Level | Hint |
| --- | --- | --- | --- |
| [Prime Multiples](https://cses.fi/problemset/task/2185) | In-class | Hard | Section 1 |
| [Fibonacci Numbers](https://cses.fi/problemset/task/1722) | In-class | Medium | Section 2 |
| [Nim Game I](https://cses.fi/problemset/task/1730) | Take-home | Easy | Section 3 |
| [Stick Game](https://cses.fi/problemset/task/1729) | Take-home | Medium | Win/lose table for 1..n |
| [Christmas Party](https://cses.fi/problemset/task/1717) | Take-home | Medium | Section 4, modulo 10^9 + 7 |
| [Tetrahedron](https://codeforces.com/problemset/problem/166/E) | Take-home | Medium | Track “at D” vs “not at D” after each step |
| [Throwing Dice](https://cses.fi/problemset/task/1096) | Take-home | Hard | Sum of the previous six terms: a 6 × 6 matrix |

### Quiz

1. How many numbers ≤ 30 are divisible by 2 or 5?
2. What is the complexity of matrix power for a recurrence using k previous terms?
3. Nim with piles 3, 5 and 6: who wins?
4. When is a game position losing?
5. What is D(4)?
