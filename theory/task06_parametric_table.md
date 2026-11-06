# Task 06: Speedup and Efficiency for alpha = 0.04

## Formulas

```
S(P) = P - alpha * (P - 1)
E(P) = S(P) / P
```

Given: `alpha = 0.04`.

## Worked example (P = 16)

```
S(16) = 16 - 0.04 * 15 = 16 - 0.6 = 15.4
E(16) = 15.4 / 16 = 0.9625
```

## Worked example (P = 1024)

```
S(1024) = 1024 - 0.04 * 1023 = 1024 - 40.92 = 983.08
E(1024) = 983.08 / 1024 = 0.96004
```

## Full table

| P | S(P) | E(P) | Cores "lost" (P - S) | Efficiency loss |
|---:|---:|---:|---:|---:|
| 16 | 15.40 | 0.96250 | 0.60 | 3.750% |
| 64 | 61.48 | 0.96063 | 2.52 | 3.938% |
| 256 | 245.80 | 0.96016 | 10.20 | 3.984% |
| 1,024 | 983.08 | 0.96004 | 40.92 | 3.996% |
| 4,096 | 3,932.20 | 0.96001 | 163.80 | 3.999% |
| 16,384 | 15,728.68 | 0.96000 | 655.32 | 4.000% |

## What the table shows

1. **Efficiency drops, but only a little.** It goes from 96.25% (P = 16) to 96.00% (P = 16,384). The total change is only 0.25 percentage points, even though P grew 1,024 times.
2. **Efficiency has a floor.** The limit is `1 - alpha = 0.96`. We reach it from above, and each step is smaller than the one before.
3. **The number of "lost" cores grows linearly.** About `0.04 * P` cores are lost. At P = 16,384 that is about 655 cores. This looks big in absolute terms, but it is the same 4% share each time.
4. **Speedup keeps growing.** Each time P is multiplied by 4, speedup is also multiplied by about 4.

## Comparison with Amdahl (same 0.04)

For fixed-size problems, Amdahl's speedup with `s = 0.04` has a ceiling of `1 / 0.04 = 25`. At P = 16,384 it would be about 25, not 15,729. This shows how different the two views are.

## Conclusion

When the problem grows with P, a 4% serial fraction costs about 4% of the machine, no matter how big the machine is. The efficiency "degradation" is tiny and flattens out fast.
