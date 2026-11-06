# Task 04: Asymptotic Analysis of Parallel Efficiency

## Definitions

```
E(P) = S(P) / P
```

We want the limit as `P -> infinity` for both laws. Assume `0 <= alpha < 1`.

## Gustafson's efficiency

Start from `S(P) = P - alpha * (P - 1)`.

```
E(P) = [P - alpha * (P - 1)] / P
     = 1 - alpha * (P - 1) / P
     = 1 - alpha * (1 - 1/P)
```

Now take the limit. As `P -> infinity`, `1/P -> 0`, so:

```
lim E(P) = 1 - alpha * (1 - 0) = 1 - alpha
P->inf
```

### Proof that the limit is correct

For any small `epsilon > 0`:

```
| E(P) - (1 - alpha) | = | -alpha * (1 - 1/P) + alpha | = alpha / P
```

This is smaller than `epsilon` when `P > alpha / epsilon`. So the limit is `1 - alpha`. QED.

### Also useful

`E(P)` goes down as P goes up, but it never goes below `1 - alpha`. The efficiency is always in the range `[1 - alpha, 1]`.

Example: for `alpha = 0.04`, `E(P)` never drops below 0.96, even for 16 million cores.

## Amdahl's efficiency

Start from `S(P) = 1 / (s + (1 - s) / P)`.

```
E(P) = S(P) / P
     = 1 / (P * s + (1 - s))
```

Now take the limit. As `P -> infinity`, `P * s -> infinity` (when `s > 0`), so:

```
lim E(P) = 1 / infinity = 0
P->inf
```

### Proof

For any `epsilon > 0`, we need `E(P) < epsilon`:

```
1 / (P * s + 1 - s) < epsilon
P * s + 1 - s > 1 / epsilon
P > (1 / epsilon - 1 + s) / s
```

A finite P exists that satisfies this, so the limit is 0. QED.

## Comparison

| | Gustafson | Amdahl |
|---|---|---|
| `lim E(P)` as P grows | `1 - alpha` | `0` |
| Speedup as P grows | grows linearly | stops at `1/s` |
| Meaning | Each core stays mostly busy | Each core becomes mostly idle |

## Numbers (alpha = s = 0.05, P = 10,000)

- Gustafson: `E = 1 - 0.05 * (9999 / 10000) = 0.95005`
- Amdahl: `E = 1 / (10000 * 0.05 + 0.95) = 1 / 500.95 = 0.0020`

Gustafson: 95% of the cores are used well. Amdahl: only 0.2%.

## Explanation

In Amdahl's model, the parallel work stays the same size while we split it into more pieces. At some point the pieces are tiny and the serial part dominates, so most cores wait. In Gustafson's model, we give every new core new work. The serial part stays the same size in absolute terms, so it takes a fixed share `alpha` of the time, and the remaining `1 - alpha` of the time keeps all cores busy.
