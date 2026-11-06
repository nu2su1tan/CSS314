# Task 08: Amdahl vs. Gustafson at the Same Fraction

## Given

- Serial fraction: `s = alpha = 0.08`
- Cores: `P = 128`

## Step 1: Amdahl's speedup

```
S_Amdahl = 1 / (s + (1 - s) / P)
         = 1 / (0.08 + 0.92 / 128)
         = 1 / (0.08 + 0.0071875)
         = 1 / 0.0871875
         = 11.47
```

## Step 2: Gustafson's scaled speedup

```
S_Gustafson = P - alpha * (P - 1)
            = 128 - 0.08 * 127
            = 128 - 10.16
            = 117.84
```

## Step 3: Compare

| Quantity | Value |
|---|---:|
| Amdahl speedup | 11.47 |
| Gustafson speedup | 117.84 |
| Difference | 106.37 |
| Ratio (Gustafson / Amdahl) | 10.27x |
| Gustafson is higher than Amdahl by | 927.4% |
| Amdahl is lower than Gustafson by | 90.3% |

Percentage formulas used:

```
(117.84 - 11.47) / 11.47  = 9.274  -> 927.4% higher
(117.84 - 11.47) / 117.84 = 0.9027 -> 90.3% lower
```

Efficiency:

- Amdahl: `11.47 / 128 = 8.96%`
- Gustafson: `117.84 / 128 = 92.06%`

## Step 4: How the gap grows with P

| P | Amdahl | Gustafson | Ratio |
|---:|---:|---:|---:|
| 16 | 7.27 | 14.80 | 2.04x |
| 64 | 10.60 | 58.96 | 5.56x |
| 128 | 11.47 | 117.84 | 10.27x |
| 1,024 | 12.36 | 942.16 | 76.22x |
| 8,192 | 12.48 | 7,536.72 | 603.78x |

## Why the two models diverge

1. **They answer different questions.** Amdahl keeps the problem size fixed, so the parallel part is cut into smaller and smaller pieces. Gustafson keeps the run time fixed, so the parallel part grows with P.
2. **Amdahl has a ceiling.** `1 / 0.08 = 12.5`. The Amdahl value gets close to this (12.48 at P = 8,192) and cannot go higher.
3. **Gustafson has no ceiling.** It is a straight line with slope `1 - alpha = 0.92`.
4. **The same number means different things.** In Amdahl, `s = 0.08` is 8% of the one-processor time. In Gustafson, `alpha = 0.08` is 8% of the parallel run time. When the problem grows, 8% of the parallel time is a very small share of the one-processor time (see Task 03). So using the same number in both formulas is not a fair comparison of one program. It is a comparison of two assumptions.

## Conclusion

At P = 128, the models differ by about 10x. At P = 8,192 they differ by about 600x. The gap keeps growing, because one curve flattens and the other keeps rising. The right model depends on whether the problem size is fixed or can grow.
