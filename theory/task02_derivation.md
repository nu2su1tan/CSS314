# Task 02: Derivation of Gustafson's Scaled Speedup

## Goal

Show that `S(P) = s + p * P`, and then that `S(P) = P - alpha * (P - 1)`.

## Setup

We run a scaled problem on P processors. We measure the time on the parallel machine.

- `s` = time spent in the serial part
- `p` = time spent in the parallel part (all P processors work at the same time)

We normalize the total parallel run time to 1:

```
s + p = 1                                  (1)
```

Here `s` and `p` are fractions of the run time on the parallel machine. We write `alpha = s` for the serial fraction.

## Step 1: Time on the parallel machine

```
T_parallel(P) = s + p = 1                  (2)
```

This follows directly from (1).

## Step 2: Time the same job would take on one processor

During the parallel part, P processors each did work that took time `p`. The total amount of parallel work is `P * p` (measured in single-processor time).

The serial part is done by one processor. It takes time `s`, and one processor needs the same time.

So one processor would need:

```
T_serial(1) = s + P * p                    (3)
```

Note: this assumes the scaled problem fits and runs on one processor in a "perfect" way. This is the standard (ideal) assumption of the model.

## Step 3: Speedup is the ratio of the two times

```
S(P) = T_serial(1) / T_parallel(P)
     = (s + P * p) / (s + p)
     = (s + P * p) / 1                     [using (1)]
     = s + p * P                           (4)
```

This is Gustafson's formula.

## Step 4: Rewrite with the serial fraction alpha

Use `s = alpha` and `p = 1 - alpha` (from equation 1):

```
S(P) = alpha + (1 - alpha) * P
     = alpha + P - alpha * P
     = P - alpha * P + alpha
     = P - alpha * (P - 1)                 (5)
```

This is the form in the task sheet.

## Check with simple numbers

Take `P = 100` and `alpha = 0.1`.

- Formula (4): `S = 0.1 + 0.9 * 100 = 90.1`
- Formula (5): `S = 100 - 0.1 * 99 = 100 - 9.9 = 90.1`

Both agree.

Check the edge cases:

- `alpha = 0` (no serial part): `S = P`. This is perfect speedup.
- `alpha = 1` (all serial): `S = 1`. No speedup, as expected.
- `P = 1`: `S = 1 - alpha * 0 = 1`. One processor gives no speedup, as expected.

## Shape of the result

`S(P)` is a straight line in P. The slope is `1 - alpha`. So every new processor adds `1 - alpha` units of speedup. This is very different from Amdahl's curve, which flattens out.
