# Task 09: Multi-Component Workload

## Given

A simulation has three phases. The percentages are shares of the total parallel run time.

| Phase | What it does | Share of time | Serial or parallel? |
|---|---|---:|---|
| A | Initial disk I/O and parameter broadcast | 2% | Serial |
| B | Boundary message-passing synchronization | 6% | Serial |
| C | Core domain flux computation | 92% | Parallel |

## Assumption

Phases A and B do not get faster when we add cores, so we count them as serial. Phase C is the compute work that every core shares, so it is the parallel part.

This is the usual reading of the task. Phase B is the arguable one (see the note at the end).

## Step 1: Aggregate serial fraction

```
alpha = A + B = 0.02 + 0.06 = 0.08
p     = C     = 0.92
check: alpha + p = 1.00
```

So `alpha = 0.08` (8%).

## Step 2: Scaled speedup for P = 512

```
S(512) = 512 - 0.08 * (512 - 1)
       = 512 - 0.08 * 511
       = 512 - 40.88
       = 471.12

E(512) = 471.12 / 512 = 0.9202  (92.02%)
```

## Step 3: Scaled speedup for P = 2,048

```
S(2048) = 2048 - 0.08 * (2048 - 1)
        = 2048 - 0.08 * 2047
        = 2048 - 163.76
        = 1884.24

E(2048) = 1884.24 / 2048 = 0.9200  (92.00%)
```

## Result

| P | S(P) | E(P) |
|---:|---:|---:|
| 512 | 471.12 | 92.02% |
| 2,048 | 1,884.24 | 92.00% |

Efficiency is almost the same for both sizes. It is close to `1 - alpha = 92%`, which is also the share of phase C.

## Per-phase view (P = 512)

Here is where the time goes on the parallel machine (total time = 1):

- A: 0.02 (serial)
- B: 0.06 (serial)
- C: 0.92 (all 512 cores busy)

One processor would need `0.08 + 512 * 0.92 = 471.12` time units for the same scaled job. This gives the same `S = 471.12`.

## Comparison with Amdahl (extra)

If the same 8% was treated as a fixed-size serial fraction:

- P = 512: `1 / (0.08 + 0.92/512) = 12.23`
- P = 2,048: `1 / (0.08 + 0.92/2048) = 12.43`

Gustafson gives about 38x and 152x more speedup, because the model assumes phase C grows with P.

## Note: what if phase B is not fully serial?

Message passing time often depends on how many cores talk to each other. It can grow with P (see Task 12). If phase B was counted as parallel, then `alpha = 0.02` and:

- `S(512) = 512 - 0.02 * 511 = 501.78`
- `S(2048) = 2048 - 0.02 * 2047 = 2007.06`

The main answer above uses `alpha = 0.08`. It is the safer (more pessimistic) choice, and it matches the task text, which asks for the "aggregate" serial fraction.
