# Task 07: Maximum Tolerable Serial Fraction

## Problem

- P = 8,192 cores
- Required scaled speedup: `S(P) >= 7,500`
- Find the largest `alpha` that still meets this.

## Derivation

Start from Gustafson's formula:

```
S(P) = P - alpha * (P - 1)
```

We need `S(P) >= S_min`:

```
P - alpha * (P - 1) >= S_min
```

Move `alpha` to one side:

```
P - S_min >= alpha * (P - 1)
```

Divide by `(P - 1)`. This number is positive, so the inequality does not flip:

```
alpha <= (P - S_min) / (P - 1)
```

So:

```
alpha_max = (P - S_min) / (P - 1)
```

## Calculation

```
alpha_max = (8192 - 7500) / (8192 - 1)
          = 692 / 8191
          = 0.084483
```

So `alpha_max = 0.08448` (about 8.45%).

## Check

With `alpha = 0.08448`:

```
S = 8192 - 0.08448 * 8191 = 8192 - 691.99 = 7500.01
```

This meets the goal.

Be careful with rounding. If we round up to `0.0845`:

```
S = 8192 - 0.0845 * 8191 = 8192 - 692.14 = 7499.86
```

This is below 7,500, so it fails. A safe value to use in practice is `alpha = 0.0844`, which gives `S = 7500.66`.

## Extra check: required efficiency

```
E_min = 7500 / 8192 = 0.9155
```

We need at least 91.55% efficiency. This matches `1 - alpha_max * (P-1)/P = 1 - 0.08448 * 0.99988 = 0.91553`.

## Result

**The serial fraction measured on the parallel machine must be at most 8.448% (exactly 692/8191).**

## Comparison with Amdahl

If we used Amdahl's Law for a fixed-size problem, a speedup of 7,500 on 8,192 cores would need:

```
1 / (s + (1 - s)/8192) >= 7500
s + (1 - s)/8192 <= 1/7500
s * (1 - 1/8192) <= 1/7500 - 1/8192
s <= (0.000133333 - 0.000122070) / 0.999878
s <= about 0.00001126
```

That is only about 0.0011%. So the same goal needs a serial fraction about 7,500 times smaller in the fixed-size view. This is why the scaled view makes large machines practical.
